def secure_archive(
    path: str, mode: int | str = "r", payload: str = ""
) -> tuple[bool, str]:
    read_mode = mode in ("r", "read", 0)
    write_mode = mode in ("w", "write", 1)
    if read_mode:
        try:
            with open(path, "r") as vault_file:
                print("Using 'secure_archive' to read from a regular file:")
                return (True, vault_file.read())
        except FileNotFoundError as error:
            print("Using 'secure_archive' to read from a nonexistent file:")
            return (False, f"{error}")
        except PermissionError as error:
            print("Using 'secure_archive' to read from an inaccessible file:")
            return (False, f"{error}")
    elif write_mode:
        try:
            with open(path, "w") as vault_file:
                vault_file.write(payload)
                print("Using 'secure_archive' to write "
                      "previous content to a new file:")
                return (True, "Content successfully written to file")
        except PermissionError as error:
            print("Using 'secure_archive' to write to an inaccessible file:")
            return (False, f"{error}")
        except Exception as error:
            return (False, f"{error}")
    else:
        return (False, "Invalid mode")


if __name__ == "__main__":
    print("=== Cyber Archives Security ===")
    print(secure_archive("/not/existing/file", "r", ""))
    print(secure_archive("/etc/master.passwd", "w", ""))
    print(secure_archive("ancient_fragment.txt", "r", ""))
    print(secure_archive(
        "ancient_fragment.txt", "w", "Vault backup restored successfully."
    ))
