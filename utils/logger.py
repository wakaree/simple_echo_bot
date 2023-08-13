from logging import INFO, basicConfig

__all__ = ["setup"]


def setup(level: int = INFO) -> None:
    basicConfig(
        format="%(asctime)s %(levelname)s | %(name)s: %(message)s",
        datefmt="[%H:%M:%S]",
        level=level,
        force=True,
    )
