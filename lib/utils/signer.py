from json import dumps
from hashlib import sha256
from .hmac import HMAC
import binascii

class Signer:
    
    def _extract_payload_element(self, json_data):
        """
        Extracts the "payload" element as a string from a JSON string.

        Args:
            json_data: The JSON string.

        Returns:
            The extracted "payload" element as a string.
        """
        start_index = json_data.find('"payload":{') + 10
        end_index = json_data.rfind(',"signature"')
        return json_data[start_index:end_index]

    def verify_signature(self, message, secret_key, signature) -> bool:
        payload = self._extract_payload_element(message)
        payload_hmac = HMAC(secret_key.encode("utf-8"), msg=payload.encode("utf-8"), digestmod=sha256).digest()
        calculated_signature = binascii.b2a_base64(payload_hmac).decode('utf-8')[:-1]     
        #print(f"calculated signature: {calculated_signature}")
        #print(f"expected   signature: {signature}")
        return calculated_signature == signature

    def get_signature(self, secret_key, payload) -> dict:
        reply_hmac = HMAC(secret_key.encode('utf-8'),
                                    dumps(payload, separators=(',', ':')).encode('utf-8'), digestmod=sha256).digest()
        encoded_hmac = binascii.b2a_base64(reply_hmac)
        return {
            "HMAC": encoded_hmac.decode('utf-8')[:-1]
        }