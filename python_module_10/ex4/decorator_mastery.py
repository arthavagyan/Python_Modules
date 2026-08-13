from functools import wraps
from typing import Callable, Any
import time


def spell_timer(func: Callable[..., Any]) -> Callable[..., Any]:

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Spell completed in {(end - start):.3f} seconds")
        return result
    return wrapper


@spell_timer
def fireball() -> str:
    time.sleep(0.1)
    return "Fireball cast!"


def power_validator(min_power: int) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            power = kwargs.get("power", args[-1])
            if power < min_power:
                return "Insufficient power for this spell"
            return func(*args, **kwargs)
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(
                        f"Spell failed, retrying... "
                        f"(attempt {attempt}/{max_attempts})")
            try:
                return func(*args, **kwargs)
            except Exception:
                return (
                    f"Spell casting failed after {max_attempts} attempts"
                )
        return wrapper
    return decorator


@retry_spell(max_attempts=3)
def unstable_spell() -> None:
    raise Exception("fizzled!")


@retry_spell(max_attempts=3)
def resilient_spell() -> str:
    return "Waaaaaaagh spelled !"


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) >= 3 and name.replace(" ", "").isalpha():
            return True
        return False

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


def main() -> None:
    print("Testing spell timer...")
    result = fireball()
    print(f"Result: {result}")

    print("\nTesting retrying spell...")
    print(unstable_spell())
    print(resilient_spell())

    print("\nTesting MageGuild...")
    guild = MageGuild()
    print(MageGuild.validate_mage_name("Merlin"))
    print(MageGuild.validate_mage_name("X"))
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Lightning", 5))


if __name__ == "__main__":
    main()
