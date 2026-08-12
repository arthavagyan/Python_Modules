import sys
import typing


def show_contents(stream: typing.IO) -> None:
    print("---")
    print(stream.read())
    print("---")


def main() -> None:
    arguments = sys.argv
    if len(arguments) == 2:
        target_path = arguments[1]
        try:
            print("=== Cyber Archives Recovery ===")
            print(f"Accessing file '{target_path}'")
            archive_file = open(target_path)
            show_contents(archive_file)
            archive_file.close()
            print(f"File '{target_path}' closed.")
        except OSError as error:
            print(f"Error opening file '{target_path}': {error}")
    else:
        print("Usage: ft_ancient_text.py <file>\n")


if __name__ == "__main__":
    main()
