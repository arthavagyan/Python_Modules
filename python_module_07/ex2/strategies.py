import abc

from ex0.creature import Creature
from ex1.capabilities import HealCapability, TransformCapability


class InvalidStrategyError(Exception):
    """Raised when a strategy cannot be used with a creature."""


class BattleStrategy(abc.ABC):
    """Define how a creature acts during a battle."""

    @abc.abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        """Return whether the strategy supports the creature."""
        pass

    @abc.abstractmethod
    def act(self, creature: Creature) -> list[str]:
        """Perform the strategy and return its action messages."""
        pass


class NormalStrategy(BattleStrategy):
    """Use a creature's normal attack."""

    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> list[str]:
        return [creature.attack()]


class DefensiveStrategy(BattleStrategy):
    """Attack and then heal."""

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> list[str]:
        if not isinstance(creature, HealCapability):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                "for this defensive strategy"
            )

        return [
            creature.attack(),
            creature.heal(),
        ]


class AggressiveStrategy(BattleStrategy):
    """Transform, attack, and then revert."""

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> list[str]:
        if not isinstance(creature, TransformCapability):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                "for this aggressive strategy"
            )

        return [
            creature.transform(),
            creature.attack(),
            creature.revert(),
        ]
