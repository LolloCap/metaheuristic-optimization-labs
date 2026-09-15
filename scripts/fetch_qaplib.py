"""Download the three QAPLIB instances used by the laboratory series."""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.request import urlopen

BASE_URL = "https://qaplib.mgi.polymtl.ca"
INSTANCES = ("tai25b", "sko90", "tai150b")


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(url, timeout=60) as response:
        destination.write_bytes(response.read())
    print(f"Downloaded {destination}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/qaplib"))
    parser.add_argument("--with-solutions", action="store_true")
    arguments = parser.parse_args()

    for name in INSTANCES:
        targets = [(f"data.d/{name}.dat", arguments.output / f"{name}.dat")]
        if arguments.with_solutions:
            targets.append((f"soln.d/{name}.sln", arguments.output / f"{name}.sln"))
        for relative_url, destination in targets:
            if destination.exists():
                print(f"Keeping existing {destination}")
                continue
            download(f"{BASE_URL}/{relative_url}", destination)


if __name__ == "__main__":
    main()
