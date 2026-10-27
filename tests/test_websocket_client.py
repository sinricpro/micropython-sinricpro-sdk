"""
Host tests for disconnect handling in sinricpro/async_websocket_client.py.

The MicroPython modules it imports are aliased to their CPython equivalents and
the socket is a fake, so these cover the client's state handling, not the transport.

    python -m unittest discover -s tests
"""
import asyncio
import binascii
import builtins
import collections
import importlib.util
import os
import random
import re
import socket
import ssl
import struct
import sys
import types
import unittest

builtins.const = lambda x: x

_uasyncio = types.ModuleType("uasyncio")
_uasyncio.__dict__.update(asyncio.__dict__)
_uasyncio.sleep_ms = lambda ms: asyncio.sleep(ms / 1000)

for _name, _mod in (("usocket", socket), ("uasyncio", _uasyncio), ("ubinascii", binascii),
                    ("urandom", random), ("ucollections", collections), ("ure", re),
                    ("ustruct", struct), ("ussl", ssl)):
    sys.modules.setdefault(_name, _mod)

_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sinricpro", "async_websocket_client.py")
_spec = importlib.util.spec_from_file_location("mpy_async_websocket_client", _PATH)
_ws_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ws_mod)

AsyncWebsocketClient = _ws_mod.AsyncWebsocketClient


class FakeSocket:
    """Non-blocking socket semantics: read() returns None while idle and b'' after the peer closes."""

    def __init__(self, incoming=b"", closed_by_peer=False, write_error=None):
        self.incoming = bytearray(incoming)
        self.closed_by_peer = closed_by_peer
        self.write_error = write_error
        self.written = bytearray()
        self.closed = False

    def read(self, size):
        if self.incoming:
            chunk = bytes(self.incoming[:size])
            del self.incoming[:size]
            return chunk
        return b"" if self.closed_by_peer else None

    def write(self, data):
        if self.write_error:
            raise self.write_error
        self.written += data

    def close(self):
        self.closed = True


def server_frame(opcode, payload=b""):
    return bytes([0x80 | opcode, len(payload)]) + payload


def connected_client(sock):
    client = AsyncWebsocketClient(ms_delay_for_read=0)
    client.sock = sock
    client._open = True
    return client


def run(coro, timeout=2):
    return asyncio.run(asyncio.wait_for(coro, timeout))


class DisconnectTests(unittest.TestCase):

    def test_recv_returns_when_peer_closes(self):
        sock = FakeSocket(closed_by_peer=True)
        client = connected_client(sock)

        self.assertIsNone(run(client.recv()))
        self.assertFalse(run(client.open()))
        self.assertTrue(sock.closed)

    def test_recv_returns_text_before_peer_close(self):
        client = connected_client(FakeSocket(server_frame(0x1, b"hello"), closed_by_peer=True))

        self.assertEqual(run(client.recv()), "hello")
        self.assertIsNone(run(client.recv()))

    def test_ping_write_reset_closes_instead_of_raising(self):
        client = connected_client(FakeSocket(write_error=OSError(104, "ECONNRESET")))
        client.ping_interval = 0

        run(client._send_ping())
        self.assertFalse(run(client.open()))

    def test_send_reset_closes_instead_of_raising(self):
        client = connected_client(FakeSocket(write_error=OSError(104, "ECONNRESET")))

        run(client.send("event"))
        self.assertFalse(run(client.open()))

    def test_silent_link_is_closed_after_unanswered_ping(self):
        sock = FakeSocket()
        client = connected_client(sock)
        client.ping_interval = 0

        run(client._send_ping())
        self.assertFalse(run(client.open()))
        self.assertEqual(sock.written[0], 0x80 | 0x9)

    def test_ping_with_payload_is_answered_with_same_payload(self):
        sock = FakeSocket(server_frame(0x9, b"abc") + server_frame(0x1, b"next"))
        client = connected_client(sock)

        self.assertEqual(run(client.recv()), "next")
        self.assertEqual(sock.written[0], 0x80 | 0xA)
        self.assertEqual(sock.written[1] & 0x7F, 3)
        mask = sock.written[2:6]
        self.assertEqual(bytes(b ^ mask[i % 4] for i, b in enumerate(sock.written[6:])), b"abc")

    def test_inbound_frame_resets_missed_ping_count(self):
        client = connected_client(FakeSocket(server_frame(0x1, b"x")))
        client.ping_missed_count = 1

        run(client.recv())
        self.assertEqual(client.ping_missed_count, 0)


if __name__ == "__main__":
    unittest.main()
