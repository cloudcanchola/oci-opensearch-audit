import logging
import sys
from typing import Literal

from rich.logging import RichHandler

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def setup_logging(
        level: LogLevel,
        use_rich: bool | None = True
) -> None:
    """
    Configure log levels and if log should use rich
    Should be called in scripts and not in utilities
    """
    # Creating initial logger and level, previous handlers will be cleared
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)

    if use_rich:
        handler = RichHandler(
            rich_tracebacks=True,
            show_time=True,
            show_level=True,
            show_path=False,
            markup=True
        )
        formatter = logging.Formatter("%(name)s | %(message)s")
        handler.setFormatter(formatter)
    else:
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)

    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
