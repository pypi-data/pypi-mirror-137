from dataclasses import dataclass
from hashlib import sha256
import json
from config import MAX_TRANSACTIONS_PER_BLOCK, TOWER_PUBLIC_KEY, HASH_LEN, PUBLIC_KEY_LEN
from transaction import Transaction


@dataclass
class BlockHeader:
    number: int
    miner_id: bytes
    parent_header_hash: bytes
    tower_signature: bytes
    transaction_hash: bytes

    def is_valid(self) -> bool:
        if self.number < 0:
            return False
        if len(self.miner_id) != PUBLIC_KEY_LEN:
            return False
        if len(self.parent_header_hash) != HASH_LEN or len(self.transaction_hash) != HASH_LEN:
            return False
        return TOWER_PUBLIC_KEY.verify(self.parent_header_hash, self.tower_signature)


@dataclass
class Block:
    header: BlockHeader
    transactions: list[Transaction]

    def __init__(
        self, miner_id: bytes, tower_signature: bytes, transactions: list[Transaction], previous_block: "Block"
    ) -> None:
        self.header = BlockHeader(
            number=previous_block.header.number + 1,
            miner_id=miner_id,
            parent_header_hash=previous_block.get_hash(),
            tower_signature=tower_signature,
            transaction_hash=get_transactions_hash(transactions),
        )
        self.transactions = transactions

    def get_hash(self) -> bytes:
        return sha256(json.dumps(self)).digest()

    def is_valid(self) -> bool:
        if not self.header.is_valid():
            return False

        if not (1 <= len(self.transactions) <= MAX_TRANSACTIONS_PER_BLOCK):
            return False

        for index, transaction in enumerate(self.transactions):
            if not transaction.is_valid(index == 0, self.header.number):
                return False

        return True


def get_transactions_hash(transactions: list[Transaction]) -> bytes:
    return sha256(json.dumps(transactions)).digest()
