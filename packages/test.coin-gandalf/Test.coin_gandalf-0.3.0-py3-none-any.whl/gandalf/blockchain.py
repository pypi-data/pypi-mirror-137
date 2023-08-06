from collections import defaultdict
from dataclasses import dataclass, field

from gandalf.block import Block


@dataclass
class BlockChainState:
    balances: dict[bytes, int] = field(default_factory=defaultdict(int))

    def forward(self, block: Block):
        for transaction in block.transactions:
            transaction.apply(self)


@dataclass
class BlockChain:
    blocks: list[Block]
    state: BlockChainState

    def forward(self, block: Block):
        self.blocks.append(block)
        self.state.forward(block)

    def get_last_block(self) -> Block:
        return self.blocks[-1]
