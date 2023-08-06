import base64
import hashlib
import json
import ecdsa

from cyberpy._wallet import privkey_to_address, privkey_to_pubkey, address_to_address



class Message:
    """A cyber message. It's possible to create transaction-like
    message and sign it. ADR 036: Arbitrary Message Signature Specification
    """

    def __init__(
        self,
        *,
        privkey: bytes,
    ) -> None:
        self._privkey = privkey
        self._msgs: list = []

    def add_message(self, signing_message: str, signer_prefix: str = 'bostrom') -> None:
        message_b64 = base64.b64encode(str.encode(signing_message)).decode("utf-8")
        msg = {
            "type": "sign/MsgSignData",
            "value": {
                "data": message_b64,
                "signer": address_to_address(privkey_to_address(self._privkey), signer_prefix)
            },
        }
        self._msgs.append(msg)

    def add_message_custom(self, signing_message_list: list, signer_prefix: str = 'bostrom') -> None:
        signing_message = ':'.join(signing_message_list)
        message_b64 = base64.b64encode(str.encode(signing_message)).decode("utf-8")
        msg = {
            "type": "sign/MsgSignData",
            "value": {
                "data": message_b64,
                "signer": address_to_address(privkey_to_address(self._privkey), signer_prefix)
            },
        }
        self._msgs.append(msg)

    def get_signed_message(self) -> dict:
        pubkey = privkey_to_pubkey(self._privkey)
        base64_pubkey = base64.b64encode(pubkey).decode("utf-8")
        return {
            "pub_key": base64_pubkey,
            "signature": self._sign()
        }

    def _sign(self) -> str:
        message_str = json.dumps(self._get_sign_message(), separators=(",", ":"), sort_keys=True)
        message_bytes = message_str.encode("utf-8")

        privkey = ecdsa.SigningKey.from_string(self._privkey, curve=ecdsa.SECP256k1)
        signature_compact = privkey.sign_deterministic(
            message_bytes, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_string_canonize
        )

        signature_base64_str = base64.b64encode(signature_compact).decode("utf-8")
        return signature_base64_str

    def _get_sign_message(self) -> dict:
        return {
            "chain_id": "",
            "account_number": "0",
            "fee": {
                "gas": "0",
                "amount": [],
            },
            "memo": '',
            "sequence": "0",
            "msgs": self._msgs,
        }