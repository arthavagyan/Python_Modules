import sys


def main() -> None:
    print("=== Command Quest ===")
    print(f"Program name: {sys.argv[0]}")

    extra_args = sys.argv[1:]
    if len(extra_args) == 0:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(extra_args)}")
        argument_number = 0
        for value in extra_args:
            argument_number += 1
            print(f"Argument {argument_number}: {value}")

    print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    main()
