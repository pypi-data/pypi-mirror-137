from __future__ import annotations

import random
from pathlib import Path

quotes_file = Path(__file__).parent / "quotes.txt"


def read_quotes() -> list[str]:
    with open(quotes_file, encoding="UTF-8") as fh:
        raw = fh.read()

    quotes = list(set(raw.split("\n------\n")))

    return quotes


def get_random_futurama_quote() -> str:
    return random.choice(read_quotes())
