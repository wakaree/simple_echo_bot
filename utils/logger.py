from logging import basicConfig, INFO


__all__ = ["setup"]


def setup() -> None:
    basicConfig(
        format="%(asctime)s %(levelname)s | %(name)s: %(message)s",
        datefmt="[%H:%M:%S]",
        level=INFO,
        force=True,
    )
