from __future__ import annotations

import random
from pathlib import Path

DB_FILE = Path(__file__).parent / "futurama_quotes.txt"


def read_db() -> list[str]:
    with open(DB_FILE, encoding="UTF-8") as fh:
        text = fh.read()

    quotes = list(set(text.split("_____")))

    return quotes


def get_random_futurama_quote() -> str:
    return random.choice(read_db())
