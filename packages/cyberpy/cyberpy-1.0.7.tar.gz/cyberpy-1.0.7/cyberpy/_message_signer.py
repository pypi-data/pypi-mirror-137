import base64
import hashlib
import json
import requests
import ecdsa

from cyberpy.interfaces.any_pb2 import Any
from cyberpy._wallet import privkey_to_address, privkey_to_pubkey
from cyberpy._typing import SyncMode


class Message:
    """A cyber message. It's possible to create transaction-like
    message in sign it.
    """

    def __init__(
        self,
        *,
        privkey: bytes,
        account_num: int,
        sequence: int,
        fee: int,
        gas: int,
        fee_denom: str = "boot",
        memo: str = "",
        chain_id: str = "space-pussy-1",
        sync_mode: SyncMode = "broadcast_tx_sync",
    ) -> None:
        self._privkey = privkey
        self._account_num = account_num
        self._sequence = sequence
        self._fee = fee
        self._fee_denom = fee_denom
        self._gas = gas
        self._memo = memo
        self._chain_id = chain_id
        self._sync_mode = sync_mode
        self._msgs: list = []

    def add_message(self, proofing_address: str, signing_doc: str) -> None:
        message = f'{proofing_address}:{signing_doc}'
        message_b64 = base64.b64encode(str.encode(message)).decode("utf-8")
        transfer = {
            "type": "sign/MsgSignData",
            "value": {
                "data": message_b64,
                "signer": privkey_to_address(self._privkey)
            },
        }
        self._msgs.append(transfer)

    def get_signed_message(self) -> str:
        pubkey = privkey_to_pubkey(self._privkey)
        base64_pubkey = base64.b64encode(pubkey).decode("utf-8")
        signed_message_raw = {
            "pub_key": base64_pubkey,
            "signature": self._sign()
        }
        signed_message_str = json.dumps(signed_message_raw, separators=(",", ":"), sort_keys=True)
        signed_message_bytes = signed_message_str.encode("utf-8")
        return base64.b64encode(signed_message_bytes).decode('utf-8')

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
            "chain_id": self._chain_id,
            "account_number": str(self._account_num),
            "fee": {
                "gas": str(self._gas),
                "amount": [{"amount": str(self._fee), "denom": self._fee_denom}],
            },
            "memo": self._memo,
            "sequence": str(self._sequence),
            "msgs": self._msgs,
        }