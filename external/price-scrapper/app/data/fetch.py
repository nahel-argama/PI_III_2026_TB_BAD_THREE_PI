import os
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

import app.env as env


def _create_data_dir() -> None:
    data_dir = get_data_dir()
    os.makedirs(f"{data_dir}/daily", exist_ok=True)
    os.makedirs(f"{data_dir}/monthly", exist_ok=True)


def get_data_dir() -> str:
    return "data"


def get_today_filename() -> str:
    tz = ZoneInfo(env.TIMEZONE)
    today = datetime.now(tz).strftime("%Y-%m-%d")
    return f"{get_data_dir()}/daily/{today}.csv"


def get_month_filename() -> str:
    tz = ZoneInfo(env.TIMEZONE)
    month = datetime.now(tz).strftime("%Y-%m")

    return f"{get_data_dir()}/monthly/{month}.csv"


async def download_daily_csv() -> str:
    filepath = get_today_filename()

    _create_data_dir()

    response = requests.get(env.PROHORT_DAILY_URL)
    response.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(response.content)

    return filepath


async def download_monthly_csv() -> str:
    filepath = get_month_filename()

    _create_data_dir()

    response = requests.get(env.PROHORT_MONTHLY_URL)
    response.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(response.content)

    return filepath


def delete_data_dir() -> None:
    data_dir = get_data_dir()

    dirs = [
        os.path.join(data_dir, "daily"),
        os.path.join(data_dir, "monthly"),
    ]

    try:
        for dir in dirs:
            for file in os.listdir(dir):
                if file.endswith(".csv"):
                    os.remove(os.path.join(dir, file))

    except Exception as e:
        raise Exception(f"Error cleaning data dir: {e}")
