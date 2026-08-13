import sys
import os


def main() -> None:
    if sys.prefix != sys.base_prefix:
        venv_path: str = os.environ.get("VIRTUAL_ENV", sys.prefix)
        venv_name: str = os.path.basename(venv_path)
        python_version = (
            f"python{sys.version_info.major}.{sys.version_info.minor}"
        )
        site_packages_path = os.path.join(
            venv_path, "lib", python_version, "site-packages"
        )

        print("MATRIX STATUS: Welcome to the construct")
        print()
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {venv_name}")
        print(f"Environment Path: {venv_path}")
        print()
        print("SUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.")
        print()
        print("Package installation path:")
        print(site_packages_path)
    else:
        print("MATRIX STATUS: You're still plugged in")
        print()
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected")
        print()
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.")
        print()
        print("To enter the construct, run:")
        print("python -m venv matrix_env")
        print("source matrix_env/bin/activate # On Unix")
        print(r"matrix_env\Scripts\activate # On Windows")
        print()
        print("Then run this program again.")


if __name__ == "__main__":
    main()
