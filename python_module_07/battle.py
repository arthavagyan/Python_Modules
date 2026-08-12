import ex0


def test_factory(factory: ex0.CreatureFactory) -> None:
    print("Testing factory")

    base_creature = factory.create_base()
    print(base_creature.describe())
    print(base_creature.attack())

    evolved_creature = factory.create_evolved()
    print(evolved_creature.describe())
    print(evolved_creature.attack())


def battle(
    first_factory: ex0.CreatureFactory,
    second_factory: ex0.CreatureFactory,
) -> None:
    print("Testing battle")

    first_creature = first_factory.create_base()
    second_creature = second_factory.create_base()

    print(first_creature.describe())
    print(" vs.")
    print(second_creature.describe())
    print(" fight!")
    print(first_creature.attack())
    print(second_creature.attack())


def main() -> None:
    flame_factory: ex0.CreatureFactory = ex0.FlameFactory()
    aqua_factory: ex0.CreatureFactory = ex0.AquaFactory()

    test_factory(flame_factory)
    print()
    test_factory(aqua_factory)
    print()
    battle(flame_factory, aqua_factory)


if __name__ == "__main__":
    main()
