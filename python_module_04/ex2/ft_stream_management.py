import sys
import typing


def annotate_lines(text: str) -> str:
    return "\n".join(line + "#" for line in text.splitlines()) + "\n"


def show_contents(stream: typing.IO) -> str:
    print("---")
    contents = stream.read()
    print(contents)
    print("---")
    return annotate_lines(contents)


def main() -> None:
    arguments = sys.argv
    if len(arguments) == 2:
        target_path = arguments[1]
        try:
            print("=== Cyber Archives Recovery & Preservation ===")
            print(f"Accessing file '{target_path}'")
            archive_file = open(target_path)
            transformed = show_contents(archive_file)
            archive_file.close()
            print(f"File '{target_path}' closed.")
            print("Transform data:")
            print(f"---\n{transformed}\n---")
            print("Enter new file name (or empty): ", end="")
            sys.stdout.flush()
            output_path = sys.stdin.readline().rstrip("\n")
            try:
                output_file = open(output_path, "w")
                print(f"Saving data to '{output_path}'")
                output_file.write(transformed)
                output_file.close()
                print(f"Data saved in file '{output_path}'.")
            except Exception as error:
                print(
                    f"[STDERR] Error opening file '{output_path}': {error}",
                    file=sys.stderr,
                )
                print("Data not saved.")
        except Exception as error:
            print(
                f"[STDERR] Error opening file '{target_path}': {error}",
                file=sys.stderr,
            )
    else:
        print("Usage: ft_ancient_text.py <file>\n")


if __name__ == "__main__":
    main()
