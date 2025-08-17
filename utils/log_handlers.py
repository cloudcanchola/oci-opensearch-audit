import json
from datetime import datetime, timedelta
from typing import Iterator

import oci.config
from oci import Response
from oci.exceptions import ServiceError
from oci.loggingsearch import LogSearchClient
from oci.loggingsearch.models import SearchLogsDetails, SearchResponse
from rich.progress import track

from utils.config import get_settings
from utils.logging_setup import get_logger
from utils.report_queries import audit_log_report

MAX_DAYS_PER_REPORT = 92
settings = get_settings()

log = get_logger(__name__)


def generate_logs_per_chunks(
        client: LogSearchClient,
        search_details: SearchLogsDetails
) -> Iterator:
    page_token = None
    data: SearchResponse = {}
    resp: Response = {}

    while True:

        try:
            resp = client.search_logs(
                search_logs_details=search_details,
                limit=1000,
                page=page_token
            )
            data = resp.data

        except ServiceError as se:
            log.error(
                "Service error: %s",
                se
            )
        except Exception as e:
            log.exception(
                "Unexpected error: %s",
                e
            )

        for entry in data.results:
            yield entry.data

        page_token = resp.next_page

        if not resp.has_next_page:
            break


def fetch_logs(
        time_start: datetime,
        time_end: datetime,
        oci_profile: str | None = "DEFAULT",
        compartment: str | None = settings.TENANCY
):
    audit_data = []
    query = audit_log_report(compartment)
    config = oci.config.from_file(profile_name=oci_profile)
    log_search_client = LogSearchClient(config=config)

    log.info("Starting log fetch...")

    # max days is 92 but oci only handles 14 days, handle in chunks
    chunk_start = time_start
    while chunk_start < time_end:
        chunk_end = min(
            chunk_start + timedelta(days=14),
            time_end
        )

        search_details = SearchLogsDetails(
            is_return_field_info=False,
            time_start=chunk_start,
            time_end=chunk_end,
            search_query=query
        )

        for entry in track(
                generate_logs_per_chunks(
                    client=log_search_client,
                    search_details=search_details
                ),
                description=f"Logs from {chunk_start} to {chunk_end}"
        ):
            # if audit_data
            audit_data.append(entry.get("data.additionalDetails"))

        chunk_start = chunk_end + timedelta(microseconds=1)

    docs = [json.loads(s) for s in audit_data]

    return docs
