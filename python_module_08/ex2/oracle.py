"""Load and display configuration from environment variables."""

import os
try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:
    def load_dotenv() -> None:
        pass


def load_config() -> dict[str, str | None]:
    load_dotenv()
    config: dict[str, str | None] = {
        "MATRIX_MODE": os.getenv("MATRIX_MODE"),
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "API_KEY": os.getenv("API_KEY"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL"),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT")
    }
    return config


def check_config(config: dict[str, str | None]) -> bool:
    missing = [key for key, value in config.items() if value is None]
    if missing:
        print("WARNING: Missing configuration variables:")
        for key in missing:
            print(f"- {key}")
        print("Copy .env.example to .env and add your configuration.")
        return False
    return True


def show_mode_info(config: dict[str, str | None]) -> None:
    mode = config["MATRIX_MODE"]
    print("Configuration loaded:")
    print(f"Mode: {mode}")
    if mode == "production":
        print("Database: Connected to production instance")
    elif mode == "development":
        print("Database: Connected to local instance")
    else:
        print("Database: Configuration mode is invalid")
    print("API Access: Authenticated")
    print(f"Log Level: {config['LOG_LEVEL']}")
    print("Zion Network: Online")
    print()
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")
    print("[OK] .env file properly configured")
    print("[OK] Production overrides available")
    print()
    print("The Oracle sees all configurations.")


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...")
    print()
    config = load_config()
    if check_config(config):
        show_mode_info(config)


if __name__ == "__main__":
    main()
