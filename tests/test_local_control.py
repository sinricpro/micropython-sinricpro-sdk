"""
Host tests for the local-control signing contract.

Runs on CPython: sinricpro/utils/signer.py and utils/hmac.py use only the
standard library, so the shipped signing code is exercised directly rather than
re-implemented. The transport itself needs MicroPython and is not covered here.

    python -m unittest discover -s tests
"""
import importlib.util
import json
import os
import sys
import types
import unittest

# Loaded by path: importing the package would pull in async_websocket_client,
# which needs usocket. utils/ itself is plain CPython.
_UTILS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sinricpro", "utils")

_pkg = types.ModuleType("mpy_utils")
_pkg.__path__ = [_UTILS]
sys.modules["mpy_utils"] = _pkg

_spec = importlib.util.spec_from_file_location(
    "mpy_utils.signer", os.path.join(_UTILS, "signer.py"))
_signer_mod = importlib.util.module_from_spec(_spec)
sys.modules["mpy_utils.signer"] = _signer_mod
_spec.loader.exec_module(_signer_mod)

Signer = _signer_mod.Signer

SECRET = "cc51b80f-0d7a-4c76-8f68-659f74d17f5d-4cd278be-3f4b-4878-82eb-a7629a0ea105"
OTHER_SECRET = "00000000-0000-4000-8000-000000000000-00000000-0000-4000-8000-000000000000"


def envelope(signer, header, payload, secret=SECRET):
    """The construction sinricpro.py uses: serialize once, splice, sign those bytes."""
    payload_json = json.dumps(payload, separators=(",", ":"))
    signature = signer.sign_payload_json(secret, payload_json)

    return '{{"header":{},"payload":{},"signature":{}}}'.format(
        json.dumps(header, separators=(",", ":")),
        payload_json,
        json.dumps(signature, separators=(",", ":")),
    )


class LocalControlSigningTest(unittest.TestCase):
    def setUp(self):
        self.signer = Signer()
        self.header = {"payloadVersion": 2, "signatureVersion": 1}
        self.payload = {
            "action": "setPowerState",
            "clientId": "test",
            "createdAt": 1788190142,
            "deviceId": "6a93e2c73ee15f85c47ed491",
            "message": "OK",
            "replyToken": "d6ba5fb3973889c6b0dd4ac1b00d92a4",
            "success": True,
            "type": "response",
            "value": {"state": "On"},
        }

    def test_signed_bytes_are_the_transmitted_bytes(self):
        raw = envelope(self.signer, self.header, self.payload)
        hmac = json.loads(raw)["signature"]["HMAC"]

        self.assertTrue(self.signer.verify_signature(raw, SECRET, hmac))

    def test_sliced_payload_matches_what_was_signed(self):
        raw = envelope(self.signer, self.header, self.payload)
        sliced = self.signer._extract_payload_element(raw)

        self.assertEqual(sliced, json.dumps(self.payload, separators=(",", ":")))

    def test_key_order_is_not_assumed(self):
        """A sender's own key order must verify: the payload is sliced, not re-encoded."""
        reordered = dict(reversed(list(self.payload.items())))
        raw = envelope(self.signer, self.header, reordered)
        hmac = json.loads(raw)["signature"]["HMAC"]

        self.assertTrue(self.signer.verify_signature(raw, SECRET, hmac))
        self.assertNotEqual(
            json.dumps(reordered, separators=(",", ":")),
            json.dumps(self.payload, separators=(",", ":")),
        )

    def test_tampered_payload_is_rejected(self):
        raw = envelope(self.signer, self.header, self.payload)
        hmac = json.loads(raw)["signature"]["HMAC"]
        tampered = raw.replace('"state":"On"', '"state":"Off"')

        self.assertNotEqual(raw, tampered)
        self.assertFalse(self.signer.verify_signature(tampered, SECRET, hmac))

    def test_wrong_secret_is_rejected(self):
        raw = envelope(self.signer, self.header, self.payload)
        hmac = json.loads(raw)["signature"]["HMAC"]

        self.assertFalse(self.signer.verify_signature(raw, OTHER_SECRET, hmac))

    def test_nested_braces_do_not_truncate_the_payload(self):
        payload = dict(self.payload)
        payload["value"] = {"outer": {"inner": {"deep": 1}}}
        raw = envelope(self.signer, self.header, payload)
        hmac = json.loads(raw)["signature"]["HMAC"]

        self.assertTrue(self.signer.verify_signature(raw, SECRET, hmac))

    def test_invalid_signature_reply_is_itself_signed(self):
        """A refusal must verify, or a client cannot trust the refusal either."""
        payload = {
            "action": "setPowerState",
            "clientId": "test",
            "createdAt": 0,
            "deviceId": "6a93e2c73ee15f85c47ed491",
            "message": "Signature is invalid",
            "replyToken": "abc",
            "success": False,
            "type": "response",
            "value": {},
        }
        raw = envelope(self.signer, self.header, payload)
        hmac = json.loads(raw)["signature"]["HMAC"]

        self.assertTrue(self.signer.verify_signature(raw, SECRET, hmac))


if __name__ == "__main__":
    unittest.main()
