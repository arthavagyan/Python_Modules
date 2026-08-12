import random

ACHIEVEMENTS: list[str] = [
    "Crafting Genius",
    "Strategist",
    "World Savior",
    "Speed Runner",
    "Survivor",
    "Master Explorer",
    "Treasure Hunter",
    "Unstoppable",
    "First Steps",
    "Collector Supreme",
    "Untouchable",
    "Sharp Mind",
    "Boss Slayer",
    "Hidden Path Finder",
]


def gen_player_achievements() -> set[str]:
    unlocked_count = random.randint(5, len(ACHIEVEMENTS) - 1)
    return set(random.sample(ACHIEVEMENTS, unlocked_count))


def main() -> None:
    print("=== Achievement Tracker System ===")
    print()

    players: dict[str, set[str]] = {
        "Alice": gen_player_achievements(),
        "Bob": gen_player_achievements(),
        "Charlie": gen_player_achievements(),
        "Dylan": gen_player_achievements(),
    }

    for name, achievements in players.items():
        print(f"Player {name}: {achievements}")
    print()

    all_achievements: set[str] = set()
    common_achievements: set[str] = set()
    is_first_player = True
    for achievements in players.values():
        all_achievements = all_achievements.union(achievements)
        if is_first_player:
            common_achievements = achievements
            is_first_player = False
        else:
            common_achievements = \
                common_achievements.intersection(achievements)
    print(f"All distinct achievements: {all_achievements}")
    print()

    print(f"Common achievements: {common_achievements}")
    print()

    for name, achievements in players.items():
        others: set[str] = set()
        for other_name, other_achievements in players.items():
            if other_name != name:
                others = others.union(other_achievements)
        print(f"Only {name} has: {achievements.difference(others)}")
    print()

    catalog = set(ACHIEVEMENTS)
    for name, achievements in players.items():
        print(f"{name} is missing: {catalog.difference(achievements)}")


if __name__ == "__main__":
    main()
