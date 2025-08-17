import argparse

import requests

from utils.config import get_settings
from utils.date_utils import parse_date
from utils.log_handlers import fetch_logs
from utils.logging_setup import setup_logging, get_logger

log = get_logger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--time-start",
        dest="time_start",
        type=parse_date,
        required=True,
    )
    parser.add_argument(
        "--time-end",
        dest="time_end",
        type=parse_date,
        required=True,
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Log level: DEBUG|INFO|WARNING|ERROR|CRITICAL (default: INFO).",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    settings = get_settings()
    setup_logging(use_rich=True, level=args.log_level)

    try:
        json_docs = fetch_logs(
            time_start=args.time_start,
            time_end=args.time_end,
        )

        resp = requests.post(settings.INGEST_URL, json=json_docs, timeout=60)
        resp.raise_for_status()
        log.info("Ingestion complete")
        return 0
    except Exception as e:
        log.exception(
            "Failed: %s",
            e
        )
        return 1


if __name__ == "__main__":
    SystemExit(main())
