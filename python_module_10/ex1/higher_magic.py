from typing import Callable


def spell(target: str, power: int) -> str:
    return f"Spell restores {target} for {power} HP"


def spell_combiner(
                   spell1: Callable[[str, int], str],
                   spell2: Callable[[str, int], str]
                   ) -> Callable[[str, int], tuple[str, str]]:
    def combine(target: str, power: int) -> tuple[str, str]:
        return (spell1(target, power), spell2(target, power))
    return combine


def power_amplifier(
                    base_spell: Callable[[str, int], str],
                    multiplier: int
                    ) -> Callable[[str, int], str]:
    def new_spell(target: str, power: int) -> str:
        new_power = power * multiplier
        return base_spell(target, new_power)
    return new_spell


def conditional_caster(
                       condition: Callable[[str, int], str],
                       spell: Callable[[str, int], str]
                       ) -> Callable[[str, int], str]:
    def new_spell(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        else:
            return "Spell fizzled"
    return new_spell


def spell_sequence(
                   spells: list[Callable[[str, int], str]]
                   ) -> Callable[[str, int], list[str]]:
    def in_order(target: str, power: int) -> list[str]:
        results: list[str] = []
        for spell in spells:
            results.append(spell(target, power))
        return results
    return in_order


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target}"


def heal(target: str, power: int) -> str:
    return f"Heals {target}"


def main() -> None:
    print()
    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    result = combined("Dragon", 10)
    print(f"Combined spell result: {result[0]}, {result[1]}")

    print()
    print("Testing power amplifier...")
    original = 10
    amplified_heal = power_amplifier(heal, 3)
    amplified_heal("Dragon", original)
    print(f"Original: {original}, Amplified: {original * 3}")


if __name__ == "__main__":
    main()
