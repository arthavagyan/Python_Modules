def ft_harvest_total() -> None:
    sum = 0
    for i in range(1, 4):
        sum += int(input(f"Day {i} harvest: "))
    print(f"Total harvest: {sum}")
