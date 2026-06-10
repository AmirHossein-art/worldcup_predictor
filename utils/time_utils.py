from datetime import datetime
from zoneinfo import ZoneInfo


IRAN_TZ = ZoneInfo("Asia/Tehran")
UTC_TZ = ZoneInfo("UTC")


def iran_to_utc(dt: datetime) -> datetime:
    """
    تبدیل datetime ساعت ایران به UTC
    """
    return (
        dt.replace(tzinfo=IRAN_TZ)
        .astimezone(UTC_TZ)
        .replace(tzinfo=None)
    )


def utc_to_iran(dt: datetime) -> datetime:
    """
    تبدیل datetime ذخیره شده (UTC) به ساعت ایران
    """
    return (
        dt.replace(tzinfo=UTC_TZ)
        .astimezone(IRAN_TZ)
    )

def format_iran_datetime(dt):
    return utc_to_iran(dt).strftime("%Y-%m-%d %H:%M")