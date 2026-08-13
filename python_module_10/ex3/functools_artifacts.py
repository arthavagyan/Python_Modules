from functools import reduce, partial, lru_cache, singledispatch
from typing import Callable, Any
import operator


def _max_op(first: int, second: int) -> int:
    if operator.gt(first, second):
        return first
    return second


def _min_op(first: int, second: int) -> int:
    if operator.lt(first, second):
        return first
    return second


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0

    operations: dict[str, Callable[[int, int], int]] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": _max_op,
        "min": _min_op,
    }

    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")

    return reduce(operations[operation], spells)


def partial_enchanter(
    base_enchantment: Callable[..., str]
) -> dict[str, Callable[..., str]]:
    return {
        "fire_enchant": partial(
            base_enchantment,
            power=50,
            element="fire"
        ),
        "ice_enchant": partial(
            base_enchantment,
            power=50,
            element="ice"
        ),
        "lightning_enchant": partial(
            base_enchantment,
            power=50,
            element="lightning"
        ),
    }


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @singledispatch
    def dispatch(target: Any) -> str:
        return "Unknown spell type"

    @dispatch.register(int)
    def _(target: int) -> str:
        return f"Damage spell: {target} damage"

    @dispatch.register(str)
    def _(target: str) -> str:
        return f"Enchantment: {target}"

    @dispatch.register(list)
    def _(target: list[Any]) -> str:
        return f"Multi-cast: {len(target)} spells"

    return dispatch


def main() -> None:
    print("Testing spell reducer...")
    spells = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(spells, 'add')}")
    print(f"Product: {spell_reducer(spells, 'multiply')}")
    print(f"Max: {spell_reducer(spells, 'max')}")

    print()

    print("Testing memoized fibonacci...")
    print(f"Fib(0): {memoized_fibonacci(0)}")
    print(f"Fib(1): {memoized_fibonacci(1)}")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")

    print()

    print("Testing spell dispatcher...")
    dispatcher = spell_dispatcher()
    print(dispatcher(42))
    print(dispatcher("fireball"))
    print(dispatcher([1, 2, 3]))
    print(dispatcher(3.14))


if __name__ == "__main__":
    main()
