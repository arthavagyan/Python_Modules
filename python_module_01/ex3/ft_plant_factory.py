class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self.height = height
        self.age = age

    def show(self) -> None:
        print(f"Created: {self.name}: {round(self.height, 1)}cm,", end="")
        print(f"{self.age}days old")


if __name__ == "__main__":
    rose = Plant("Rose", 25.0, 30)
    oak = Plant("Oak", 200.0, 365)
    cactus = Plant("Cactus", 5.0, 90)
    sunflower = Plant("Sunflower", 80.0, 45)
    fern = Plant("Fern", 15.0, 120)
    print("=== Plant Factory Output ===")
    plants = [rose, oak, cactus, sunflower, fern]
    for plant in plants:
        plant.show()
