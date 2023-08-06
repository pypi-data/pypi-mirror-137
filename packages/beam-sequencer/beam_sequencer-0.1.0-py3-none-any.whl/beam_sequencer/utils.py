import re

from typing import Dict


MINUTE_S = 60
HOUR_S = 60 * MINUTE_S
DAY_S = 24 * HOUR_S
WEEK_S = 7 * DAY_S
MONTH_S = 30 * DAY_S
YEAR_S = 365 * DAY_S


def iso8601_duration_parser(duration: str) -> int:
    """
    Parses a string in ISO-8601 duration format 
    and returns the number of seconds.

    input: P30D
    output: 86400
    """
    iso8601_pattern = re.compile(
        r"^(?P<sign>[+-])?"
        r"P(?!\b)"
        r"(?P<years>[0-9]+([,.][0-9]+)?Y)?"
        r"(?P<months>[0-9]+([,.][0-9]+)?M)?"
        r"(?P<weeks>[0-9]+([,.][0-9]+)?W)?"
        r"(?P<days>[0-9]+([,.][0-9]+)?D)?"
        r"((?P<separator>T)(?P<hours>[0-9]+([,.][0-9]+)?H)?"
        r"(?P<minutes>[0-9]+([,.][0-9]+)?M)?"
        r"(?P<seconds>[0-9]+([,.][0-9]+)?S)?)?$"
    )

    match = iso8601_pattern.match(duration).groupdict()
    units: Dict[str, int] = {}
    for key, value in match.items():
        if key not in ("separator", "sign"):
            units[key] = int(value[:-1]) if value else 0

    seconds = (
        (units["years"] * YEAR_S)
        + (units["months"] * MONTH_S)
        + (units["weeks"] * WEEK_S)
        + (units["days"] * DAY_S)
        + (units["hours"] * HOUR_S)
        + (units["minutes"] * MINUTE_S)
        + units["seconds"]
    )
    return seconds
