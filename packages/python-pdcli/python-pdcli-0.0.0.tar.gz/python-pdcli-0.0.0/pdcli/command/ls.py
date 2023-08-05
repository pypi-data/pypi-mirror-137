"""Implement pd ls command."""
import datetime
from typing import List
import json
from csv import DictWriter
import io

from ..api.incident import Status, Urgency, list_incidents


def ls(  # pylint: disable=invalid-name
    *,
    since: str = None,
    statuses: List[str] = None,
    user_ids: List[str] = None,
    urgency: str = None,
    column: bool = False,
    delimiter: str = "\t",
) -> str:
    """List incidents.

    :param since: since date
    :param statuses: filter by statuses
    :param user_ids: filter by user id if provided
    :param urgency: filter by urgency if provided
    :param column: return rows of columns, instead of json string
    :param delimiter: delimiter used for column output
    """
    if statuses:
        if isinstance(statuses, str):
            statuses = [statuses]
    else:
        statuses = []

    if user_ids:
        if isinstance(user_ids, str):
            user_ids = [user_ids]
    else:
        user_ids = []

    incidents = list_incidents(
        since=datetime.date.fromisoformat(since) if since else None,
        statuses=[Status(status) for status in statuses],
        user_ids=user_ids,
        urgency=Urgency(urgency) if urgency else None,
    )

    if column:
        return _as_columns(
            incidents=incidents,
            columns=[
                "status",
                "urgency",
                "title",
                "created_at",
                "service",
                "assignments",
            ],
            delimiter=delimiter,
        )

    return json.dumps(incidents)


def _as_columns(*, incidents, columns, delimiter):

    column_transforms = {
        "service": lambda x: x["summary"],
        "assignments": lambda x: ", ".join(
            assignment["assignee"]["summary"] for assignment in x
        ),
    }

    def filter_fields(incident):
        row = {}

        for column in columns:
            if column not in incident.keys():
                continue
            value = incident[column]
            if transform := column_transforms.get(column):
                value = transform(value)
            row[column] = value

        return row

    rows = [filter_fields(incident) for incident in incidents]

    with io.StringIO() as file_:
        writer = DictWriter(file_, fieldnames=columns, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)

        return file_.getvalue()
