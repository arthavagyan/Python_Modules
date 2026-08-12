from ex0 import AquaFactory, CreatureFactory, FlameFactory
from ex0.creature import Creature
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    AggressiveStrategy,
    BattleStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
    NormalStrategy,
)


Opponent = tuple[CreatureFactory, BattleStrategy]
PreparedOpponent = tuple[Creature, BattleStrategy]


def battle(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    creatures: list[PreparedOpponent] = []

    for factory, strategy in opponents:
        creature: Creature = factory.create_base()
        creatures.append((creature, strategy))

    try:
        for first_index in range(len(creatures)):
            for second_index in range(
                first_index + 1,
                len(creatures),
            ):
                first_creature, first_strategy = creatures[first_index]
                second_creature, second_strategy = creatures[second_index]

                print()
                print("* Battle *")
                print(first_creature.describe())
                print(" vs.")
                print(second_creature.describe())
                print(" now fight!")

                first_actions: list[str] = first_strategy.act(
                    first_creature
                )
                for action in first_actions:
                    print(action)

                second_actions: list[str] = second_strategy.act(
                    second_creature
                )
                for action in second_actions:
                    print(action)

    except InvalidStrategyError as error:
        print(f"Battle error, aborting tournament: {error}")


def main() -> None:
    print("Tournament 0 (basic)")
    print(" [ (Flameling+Normal), (Healing+Defensive) ]")

    battle([
        (FlameFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
    ])

    print("\nTournament 1 (error)")
    print(" [ (Flameling+Aggressive), (Healing+Defensive) ]")

    battle([
        (FlameFactory(), AggressiveStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
    ])

    print("\nTournament 2 (multiple)")
    print(
        " [ (Aquabub+Normal), "
        "(Healing+Defensive), "
        "(Transform+Aggressive) ]"
    )

    battle([
        (AquaFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
        (TransformCreatureFactory(), AggressiveStrategy()),
    ])


if __name__ == "__main__":
    main()
