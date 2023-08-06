import json
from hashlib import sha256

from base58 import b58decode

from config import MAX_DATA_SIZE, PUBLIC_KEY_LEN
from nacl.signing import VerifyKey
from dataclasses import dataclass

BLOCKCHAIN_STATE_TYPE = ""


@dataclass
class TransactionContent:
    from_addr: bytes
    to_addr: bytes
    fees: int
    amount: int
    data: bytes

    def is_valid(self) -> bool:
        if len(self.data) > MAX_DATA_SIZE:
            return False
        if len(self.from_addr) != PUBLIC_KEY_LEN or len(self.to_addr) != PUBLIC_KEY_LEN:
            return False
        if self.amount < 0 or self.fees < 0:
            return False

        return True


@dataclass
class Transaction:
    content: TransactionContent
    signature: bytearray

    def is_valid(self, is_fist_block_transaction: bool, block_numer: int) -> bool:
        if not self.content.is_valid():
            return False

        if is_fist_block_transaction:
            return self.is_valid_miner_transaction(block_numer)

        verifier = VerifyKey(b58decode(self.content.from_addr))
        if not verifier.verify(bytes(self.get_hash()), self.signature):
            return False

        return True

    def get_hash(self) -> bytes:
        return sha256(json.dumps(self)).digest()

    def is_valid_miner_transaction(self, block_number: int) -> bool:
        if self.content.fees != 0:
            return False

        if self.content.amount > get_minable_account(block_number):
            return False

        return True

    def can_be_applied(self, state: BLOCKCHAIN_STATE_TYPE, is_first_block_transaction: bool) -> bool:
        if is_first_block_transaction:
            return True

        balance = state.balances.get(self.content.from_addr)
        if balance is None:
            return False
        return balance >= self.content.amount + self.content.fees

    def apply_miner_transaction(self, state: BLOCKCHAIN_STATE_TYPE):
        pass


def get_minable_account(block_number: int) -> int:
    if 0 <= block_number <= 16:
        return 100_000_00
    return 100_00
