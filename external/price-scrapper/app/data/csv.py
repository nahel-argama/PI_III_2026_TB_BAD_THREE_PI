from zoneinfo import ZoneInfo
from os import path
from datetime import datetime, timedelta

import requests

from app import env


class CsvDownloadException(Exception):
    pass


class CsvStoreException(Exception):
    pass


def get_and_prepare_csv() -> str:
    if should_download_csv():
        try:
            csv_data = download_csv()
            csv_path = get_csv_current_week_path()
            store_csv(csv_data, csv_path)
            return csv_data

        except (CsvDownloadException, CsvStoreException) as e:
            raise CsvDownloadException(f"Error occurred while preparing CSV: {e}")

    try:
        csv_data = get_csv_file_data()
        return csv_data
    except (CsvDownloadException, CsvStoreException) as e:
        raise CsvDownloadException(f"Error occurred while preparing CSV: {e}")


def get_csv_week_csv_name(offset: int = 0) -> str:
    today = datetime.now().date()
    tz = ZoneInfo("America/Sao_Paulo")

    now_date = datetime(today.year, today.month, today.day).astimezone(tz).date()
    week_start = (
        now_date - timedelta(days=now_date.weekday() + 1) + timedelta(weeks=offset)
    )
    week_end = week_start + timedelta(days=6)

    return f"{week_start}_{week_end}.csv"


def get_stored_csv_files() -> list[str]:
    try:
        import os

        csv_files = []
        for root, _, files in os.walk("data"):
            for file in files:
                if file.endswith(".csv"):
                    csv_files.append(os.path.join(root, file))

        csv_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        return csv_files
    except Exception as e:
        raise CsvDownloadException(
            f"Error occurred while listing stored CSV files: {e}"
        )


def get_csv_current_week_path() -> str:
    return f"data/{get_csv_current_week_csv_name()}"


def get_csv_file_data() -> str:
    try:
        with open(get_csv_current_week_path(), "r") as f:
            return f.read()
    except FileNotFoundError:
        raise CsvDownloadException("CSV file not found for the current week.")
    except Exception as e:
        raise CsvDownloadException(str(e))


def should_download_csv() -> bool:
    csv_path = get_csv_current_week_path()

    try:
        if not path.exists(csv_path):
            return True

        return False
    except FileNotFoundError:
        return True
    except Exception as e:
        raise CsvDownloadException(f"Error occurred while reading current CSV: {e}")


def download_csv() -> str:
    try:
        response = requests.get(env.CSV_URL)

        return response.text
    except requests.RequestException as e:
        raise CsvDownloadException(str(e))


def store_csv(data: str, file_path: str) -> None:
    if "/" in file_path:
        directory = file_path.rsplit("/", 1)[0]
        try:
            import os

            os.makedirs(directory, exist_ok=True)
        except Exception as e:
            raise CsvStoreException(str(e))

    try:
        with open(file_path, "w") as f:
            f.write(data)
    except Exception as e:
        raise CsvStoreException(str(e))
