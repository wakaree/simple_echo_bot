
from logging import (
    basicConfig, StreamHandler,
    Handler, INFO, FileHandler
)
from typing import List


__all__ = ["setup"]


def setup() -> None:
    handlers: List[Handler] = [
        StreamHandler(),
        FileHandler("logs.log", encoding="utf-8")
    ]

    basicConfig(
        format='%(asctime)s %(levelname)s | %(name)s: %(message)s',
        datefmt='[%H:%M:%S]',
        level=INFO,
        force=True,
        handlers=handlers
    )
