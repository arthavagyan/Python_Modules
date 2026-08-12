class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown water error") -> None:
        super().__init__(message)


def wilt_plant() -> None:
    raise PlantError("The tomato plant is wilting!")


def drain_water_tank() -> None:
    raise WaterError("Not enough water in the tank!")


def test_custom_errors() -> None:
    print("=== Custom Garden Errors Demo ===")
    print()

    print("Testing PlantError...")
    try:
        wilt_plant()
    except PlantError as exc:
        print(f"Caught PlantError: {exc}")
    print()

    print("Testing WaterError...")
    try:
        drain_water_tank()
    except WaterError as exc:
        print(f"Caught WaterError: {exc}")
    print()

    print("Testing catching all garden errors...")
    for cause_trouble in (wilt_plant, drain_water_tank):
        try:
            cause_trouble()
        except GardenError as exc:
            print(f"Caught GardenError: {exc}")
    print()

    print("All custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()
