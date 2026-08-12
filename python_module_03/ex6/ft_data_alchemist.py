import random

PLAYER_NAMES = [
    "Alice", "bob", "Charlie", "dylan", "Emma",
    "Gregory", "john", "kevin", "Liam",
]


def main() -> None:
    print("=== Game Data Alchemist ===")
    print()

    print(f"Initial list of players: {PLAYER_NAMES}")

    capitalized_names = [name.capitalize() for name in PLAYER_NAMES]
    print(f"New list with all names capitalized: {capitalized_names}")

    already_capitalized = [
        name for name in PLAYER_NAMES if name == name.capitalize()
    ]
    print(f"New list of capitalized names only: {already_capitalized}")
    print()

    scores = {name: random.randint(0, 999) for name in capitalized_names}
    print(f"Score dict: {scores}")

    average_score = round(sum(scores.values()) / len(scores), 2)
    print(f"Score average is {average_score}")

    high_scores = {
        name: score for name, score in scores.items() if score > average_score
    }
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    main()
