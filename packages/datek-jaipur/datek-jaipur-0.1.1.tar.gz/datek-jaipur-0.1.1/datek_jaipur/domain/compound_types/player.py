from dataclasses import dataclass

from datek_jaipur.domain.compound_types.card import CardSet
from datek_jaipur.domain.simple_types import Name, Number, Amount


@dataclass(frozen=True)
class Player:
    name: Name
    score: Number
    goods: CardSet
    herd: CardSet

    def __eq__(self, other):
        return self.name == other.name if isinstance(other, Player) else False


@dataclass
class PlayerCreatedEventInput:
    name: Name
    score: Amount
    goods: CardSet
    herd: CardSet
