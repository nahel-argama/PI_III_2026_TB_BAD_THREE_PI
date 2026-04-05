from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def main():
    day = int(input())
    month = int(input())
    year = int(input())

    tz = ZoneInfo("America/Sao_Paulo")

    now_date = datetime(year, month, day).astimezone(tz).date()
    week_start = now_date - timedelta(days=now_date.weekday() + 1)
    week_end = week_start + timedelta(days=6)

    print(f"data_{week_start}_{week_end}.csv")


main()
