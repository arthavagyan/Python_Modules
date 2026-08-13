from typing import Any


def artifact_sorter(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        artifacts, key=lambda artifact: artifact["power"], reverse=True
    )


def power_filter(
                mages: list[dict[str, Any]], min_power: int
                ) -> list[dict[str, Any]]:
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: "* " + spell + " *", spells))


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, Any]:
    total = sum(list(map(lambda mage: mage["power"], mages)))
    return {
        "max_power": max(mages, key=lambda mage: mage["power"])["power"],
        "min_power": min(mages, key=lambda mage: mage["power"])["power"],
        "avg_power": round(total / len(mages), 2)
           }


def main() -> None:
    artifacts = ([
        {"name": "Fire Staff", "power": 92, "type": "weapon"},
        {"name": "Crystal Orb", "power": 85, "type": "orb"},
        {"name": "Dark Blade", "power": 78, "type": "weapon"}
    ])
    spells = ["fireball", "heal", "shield"]

    print()
    print("Testing artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    print(
        f"{sorted_artifacts[0]['name']} ({sorted_artifacts[0]['power']} power)"
        f" comes before {sorted_artifacts[1]['name']}"
        f" ({sorted_artifacts[1]['power']} power)")

    print()
    print("Testing spell transformer...")
    transformed = spell_transformer(spells)
    print(" ".join(transformed))


if __name__ == "__main__":
    main()
