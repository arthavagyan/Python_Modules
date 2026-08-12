import sys


def parse_inventory(arguments: list[str]) -> dict[str, int]:
    inventory: dict[str, int] = {}

    for argument in arguments:
        if ":" not in argument:
            print(f"Error - invalid parameter '{argument}'")
            continue

        item_name, quantity_text = argument.split(":", 1)
        if item_name in inventory:
            print(f"Redundant item '{item_name}' - discarding")
            continue

        try:
            quantity = int(quantity_text)
        except ValueError as exc:
            print(f"Quantity error for '{item_name}': {exc}")
            continue

        inventory[item_name] = quantity

    return inventory


def main() -> None:
    print("=== Inventory System Analysis ===")

    inventory = parse_inventory(sys.argv[1:])
    print(f"Got inventory: {inventory}")

    item_names = list(inventory.keys())
    print(f"Item list: {item_names}")

    if len(item_names) == 0:
        return

    total_quantity = sum(inventory.values())
    print(f"Total quantity of the {len(inventory)} items: {total_quantity}")

    for item_name, quantity in inventory.items():
        share = round(quantity / total_quantity * 100, 1)
        print(f"Item {item_name} represents {share}%")

    most_abundant_name = item_names[0]
    least_abundant_name = item_names[0]
    for item_name, quantity in inventory.items():
        if quantity > inventory[most_abundant_name]:
            most_abundant_name = item_name
        if quantity < inventory[least_abundant_name]:
            least_abundant_name = item_name
    print(
        f"Item most abundant: {most_abundant_name} "
        f"with quantity {inventory[most_abundant_name]}"
    )
    print(
        f"Item least abundant: {least_abundant_name} "
        f"with quantity {inventory[least_abundant_name]}"
    )

    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
