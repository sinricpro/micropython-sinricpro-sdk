import uasyncio
import socket

from .utils.logging import getLogger

UDP_PORT = 3333
UDP_MULTICAST_IP = '224.9.9.9'

# Not exported by every MicroPython port; the value is fixed by lwIP.
_IP_ADD_MEMBERSHIP = getattr(socket, 'IP_ADD_MEMBERSHIP', 3)

_POLL_MS = 50
_MAX_DATAGRAM = 1024


def _packed_ip(address):
    return bytes(int(part) for part in address.split('.'))


class UdpListener:
    """
    Answers signed SinricPro commands over the LAN.

    Bound to INADDR_ANY rather than the multicast group: the same socket then
    takes unicast and subnet broadcast, and broadcast is how a client finds the
    device on networks that drop multicast.
    """

    def __init__(self, received_queue):
        self.received_queue = received_queue
        self.logger = getLogger("SinricPro")
        self._sock = None

    def start(self) -> bool:
        if self._sock:
            return True

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('0.0.0.0', UDP_PORT))
            sock.setblocking(False)
        except Exception as e:
            self.logger.error('UDP: cannot listen on {}: {}'.format(UDP_PORT, e))
            return False

        # A failed group join still leaves a usable socket for unicast and
        # broadcast, so it is logged rather than treated as fatal.
        try:
            mreq = _packed_ip(UDP_MULTICAST_IP) + bytes(4)
            sock.setsockopt(socket.IPPROTO_IP, _IP_ADD_MEMBERSHIP, mreq)
            joined = True
        except Exception as e:
            self.logger.error('UDP: could not join {}: {}'.format(UDP_MULTICAST_IP, e))
            joined = False

        self._sock = sock
        self.logger.info('UDP: listening on {}, multicast joined={}'.format(UDP_PORT, joined))
        return True

    async def run(self) -> None:
        """Polls the socket; MicroPython has no portable reader callback."""
        while self._sock:
            try:
                data, peer = self._sock.recvfrom(_MAX_DATAGRAM)
            except OSError:
                await uasyncio.sleep_ms(_POLL_MS)
                continue
            except Exception as e:
                self.logger.error('UDP: receive failed: {}'.format(e))
                await uasyncio.sleep_ms(_POLL_MS)
                continue

            if not data:
                continue

            try:
                message = data.decode('utf-8')
            except Exception:
                continue

            # The peer travels with the message: a response can leave several
            # loop iterations later, by which time another peer may have sent.
            self.received_queue.put((message, peer))
            await uasyncio.sleep(0)

    def send(self, message, peer) -> None:
        """Reply on the listening socket; a second socket does not transmit on lwIP."""
        if not self._sock or not peer:
            return

        try:
            self._sock.sendto(message.encode('utf-8'), peer)
        except Exception as e:
            self.logger.error('UDP: reply to {} failed: {}'.format(peer, e))

    def stop(self) -> None:
        if not self._sock:
            return

        try:
            self._sock.close()
        except Exception:
            pass

        self._sock = None
