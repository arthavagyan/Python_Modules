def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    save = seed_type.capitalize()
    if unit == "packets":
        print(f"{save} seeds: {quantity} {unit} available")
    elif unit == "grams":
        print(f"{save} seeds: {quantity} {unit} total")
    elif unit == "area":
        print(f"{save} seeds: covers {quantity} square meters")
    else:
        print("Unknown unit type")
