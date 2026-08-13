import importlib

PACKAGE_DESCRIPTIONS: dict[str, str] = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "requests": "Network access ready",
    "matplotlib": "Visualization ready"
}


def check_dependencies() -> dict[str, bool]:
    availability: dict[str, bool] = {}

    for name in PACKAGE_DESCRIPTIONS:
        try:
            module = importlib.import_module(name)
            print(
                f"[OK] {name} ({module.__version__}) - "
                f"{PACKAGE_DESCRIPTIONS[name]}"
            )
            availability[name] = True
        except ImportError:
            availability[name] = False
            print(f"[MISSING] {name}")
            print(f"  Install with pip: pip install {name}")
            print(f"  Install with poetry: poetry add {name}")

    return availability


def compare_pip_poetry() -> None:
    print()
    print("Dependency management comparison:")
    print("  pip:")
    print("    - uses requirements.txt")
    print("    - does not automatically lock versions")
    print("    - installs packages directly into the active environment")
    print("  poetry:")
    print("    - uses pyproject.toml and poetry.lock")
    print("    - automatically resolves and locks exact versions")
    print("    - creates and manages the virtual environment for you")
    print()


def main() -> None:
    print("LOADING STATUS: Loading programs...")
    print()
    print("Checking dependencies:")
    availability: dict[str, bool] = check_dependencies()
    compare_pip_poetry()

    required = ["numpy", "pandas", "matplotlib"]
    missing = [name for name in required if not availability[name]]
    if missing:
        print(f"Cannot proceed without {missing[0]}")
        return

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    print("Analyzing Matrix data...")
    matrix_samples = np.random.randn(1000)
    print(f"Processing {len(matrix_samples)} data points...")

    df = pd.DataFrame({"Matrix_Numbers": matrix_samples})

    print("Generating visualization...")
    plt.hist(df["Matrix_Numbers"], bins=30)
    plt.savefig("matrix_analysis.png")
    print()

    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    main()
