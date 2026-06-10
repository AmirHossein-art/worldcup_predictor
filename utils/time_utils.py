from datetime import datetime
from zoneinfo import ZoneInfo

import jdatetime


IRAN_TZ = ZoneInfo("Asia/Tehran")
UTC_TZ = ZoneInfo("UTC")

WEEKDAYS = {
    "Saturday": "شنبه",
    "Sunday": "یکشنبه",
    "Monday": "دوشنبه",
    "Tuesday": "سه‌شنبه",
    "Wednesday": "چهارشنبه",
    "Thursday": "پنجشنبه",
    "Friday": "جمعه",
}


def iran_to_utc(dt: datetime) -> datetime:
    """
    تبدیل ساعت ایران به UTC برای ذخیره در دیتابیس
    """
    return (
        dt.replace(tzinfo=IRAN_TZ)
        .astimezone(UTC_TZ)
        .replace(tzinfo=None)
    )


def utc_to_iran(dt: datetime) -> datetime:
    """
    تبدیل UTC به ساعت ایران
    """
    return (
        dt.replace(tzinfo=UTC_TZ)
        .astimezone(IRAN_TZ)
    )


def format_shamsi_datetime(dt: datetime) -> str:
    iran_dt = utc_to_iran(dt)

    shamsi = jdatetime.datetime.fromgregorian(
        datetime=iran_dt
    )

    weekday = WEEKDAYS[
        iran_dt.strftime("%A")
    ]

    return (
        f"{weekday} | "
        f"{shamsi.strftime('%Y/%m/%d')} | "
        f"{iran_dt.strftime('%H:%M')}"
    )

def format_shamsi_date(dt: datetime) -> str:
    """
    فقط تاریخ شمسی
    """
    iran_dt = utc_to_iran(dt)

    shamsi = jdatetime.datetime.fromgregorian(
        datetime=iran_dt
    )

    return shamsi.strftime(
        "%Y/%m/%d"
    )


def format_shamsi_time(dt: datetime) -> str:
    """
    فقط ساعت
    """
    iran_dt = utc_to_iran(dt)

    return iran_dt.strftime("%H:%M")