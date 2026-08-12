def input_temperature(temp_str: str) -> int:
    temperature = int(temp_str)
    if temperature > 40:
        raise ValueError(f"{temperature}°C is too hot for plants (max 40°C)")
    if temperature < 0:
        raise ValueError(f"{temperature}°C is too cold for plants (min 0°C)")
    return temperature


def test_temperature() -> None:
    print("=== Garden Temperature Checker ===")
    print()

    for sample in ("25", "abc", "100", "-50"):
        print(f"Input data is '{sample}'")
        try:
            temperature = input_temperature(sample)
            print(f"Temperature is now {temperature}°C")
        except ValueError as exc:
            print(f"Caught input_temperature error: {exc}")
        print()

    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
