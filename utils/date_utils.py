
import argparse
from datetime import datetime

DATE_FORMAT_INPUT = "%Y-%m-%d"
MAX_DAYS_PER_REPORT = 92


def parse_date(s: str) -> datetime:
    """
    Parses a YYYY-MM-DD string into a datetime object at midnight.
    Raises argparse.ArgumentTypeError on invalid format (para argparse).
    """
    try:
        return datetime.strptime(s, DATE_FORMAT_INPUT)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date '{s}'. Expected format: YYYY-MM-DD"
        )


def validate_date_range(time_start: datetime, time_end: datetime) -> None:
    if time_start > time_end:
        raise ValueError("--time-start must be lower than --time-end")

    delta_days = (time_end - time_start).days + 1
    if delta_days > MAX_DAYS_PER_REPORT:
        raise ValueError(
            f"Date range too large: {delta_days} days. "
            f"Max allowed is {MAX_DAYS_PER_REPORT} days."
        )
