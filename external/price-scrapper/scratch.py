from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def main():
    offset = int(input())

    print(get_csv_week_csv_name(offset))


def get_csv_week_csv_name(offset: int = 0) -> str:
    today = datetime.now().date()
    tz = ZoneInfo("America/Sao_Paulo")

    now_date = datetime(today.year, today.month, today.day).astimezone(tz).date()
    week_start = (
        now_date - timedelta(days=now_date.weekday() + 1) + timedelta(weeks=offset)
    )
    week_end = week_start + timedelta(days=6)

    return f"{week_start}_{week_end}.csv"


if __name__ == "__main__":
    main()
