def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def test_temperature() -> None:
    print("=== Garden Temperature ===")
    print()

    for sample in ("25", "abc"):
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
