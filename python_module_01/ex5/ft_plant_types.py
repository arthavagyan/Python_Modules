class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name: str = name
        self.height: float = height
        self.age: int = age

    def show(self, first: bool = True) -> None:
        if first:
            print(f"=== {type(self).__name__}")
        print(f"{self.name}: {round(self.height, 1)}cm, {self.age} days old")


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, color: str) -> None:
        super().__init__(name, height, age)
        self.color: str = color
        self.blooming: int = 0

    def bloom(self) -> None:
        self.blooming = 1

    def show(self, first: bool = True) -> None:
        super().show(first)
        print(f"Color: {self.color}")
        if self.blooming == 1:
            print(f"{self.name} is blooming beautifully!")
        else:
            print(f"{self.name} has not bloomed yet")


class Tree(Plant):
    def __init__(
        self,
        name: str,
        height: float,
        age: int,
        diameter: float
    ) -> None:
        super().__init__(name, height, age)
        self.diameter: float = diameter

    def produce_shade(self) -> None:
        print(
            f"Tree {self.name} now produces a shade of {self.height}cm "
            f"long and {self.diameter}cm wide"
        )

    def show(self, first: bool = True) -> None:
        super().show(first)
        print(f"Trunk diameter: {self.diameter}cm")


class Vegetable(Plant):
    def __init__(
            self,
            name: str,
            height: float,
            age: int,
            harvest_season: str) -> None:
        super().__init__(name, height, age)
        self.nutrit: int = 0
        self.harvest_season: str = harvest_season

    def age_of_plant(self) -> None:
        self.age += 1

    def grow(self) -> None:
        self.height += 2.1
        self.nutrit += 1

    def show(self, first: bool = True) -> None:
        super().show(first)
        print(f"Harvest season: {self.harvest_season}")
        print(f"Nutritional value: {self.nutrit}")


if __name__ == "__main__":
    rose: Flower = Flower("Rose", 15.0, 10, "red")
    oak: Tree = Tree("Oak", 200.0, 365, 5.0)
    tomato: Vegetable = Vegetable("Tomato", 5.0, 10, "April")

    print("=== Garden Plant Types ===")

    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show(first=False)

    print("\n")

    oak.show()
    print("[asking the oak to produce shade]")
    oak.produce_shade()

    print("\n")

    tomato = Vegetable("Tomato", 5.0, 10, "April")
    tomato.show()
    print("[make tomato grow and age for 20 days]")

    for i in range(20):
        tomato.grow()
        tomato.age_of_plant()

    tomato.show(first=False)
