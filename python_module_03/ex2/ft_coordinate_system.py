import math

Coordinates = tuple[float, float, float]


def get_player_pos() -> Coordinates:
    while True:
        raw_line = input("Enter new coordinates as floats in format 'x,y,z': ")
        try:
            x_text, y_text, z_text = raw_line.split(",")
        except ValueError:
            print("Invalid syntax")
            continue

        x_text, y_text, z_text = x_text.strip(), y_text.strip(), z_text.strip()
        try:
            x = float(x_text)
        except ValueError as exc:
            print(f"Error on parameter '{x_text}': {exc}")
            continue
        try:
            y = float(y_text)
        except ValueError as exc:
            print(f"Error on parameter '{y_text}': {exc}")
            continue
        try:
            z = float(z_text)
        except ValueError as exc:
            print(f"Error on parameter '{z_text}': {exc}")
            continue

        return x, y, z


def distance(origin: Coordinates, target: Coordinates) -> float:
    return math.sqrt(
        (target[0] - origin[0]) ** 2
        + (target[1] - origin[1]) ** 2
        + (target[2] - origin[2]) ** 2
    )


def main() -> None:
    print("=== Game Coordinate System ===")
    print()

    print("Get a first set of coordinates")
    first = get_player_pos()
    print(f"Got a first tuple: {first}")
    print(f"It includes: X={first[0]}, Y={first[1]}, Z={first[2]}")
    center: Coordinates = (0.0, 0.0, 0.0)
    print(f"Distance to center: {round(distance(first, center), 4)}")
    print()

    print("Get a second set of coordinates")
    second = get_player_pos()
    print(
        "Distance between the 2 sets of coordinates: "
        f"{round(distance(first, second), 4)}"
    )


if __name__ == "__main__":
    main()
