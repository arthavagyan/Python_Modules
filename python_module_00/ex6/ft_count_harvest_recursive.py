def ft_count_harvest_recursive() -> None:
    a = int(input("Days until harvest: "))

    def helper(b):
        if b > a:
            return
        print(f"Day {b}")
        helper(b + 1)
    helper(1)
    print("Harvest time!")
