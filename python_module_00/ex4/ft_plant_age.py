def ft_plant_age() -> None:
    a = int(input("Enter plant age in days: "))
    if a > 60:
        print("Plant is ready to harvest!")
    elif a <= 60:
        print("Plant needs more time to grow.")
