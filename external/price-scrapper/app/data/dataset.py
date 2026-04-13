import datetime
from zoneinfo import ZoneInfo

import pandas as pd

from app import env
from app.data.fetch import get_today_filename, get_month_filename
from app.database.products import PriceFrequency


async def get_data_frame_from_csv(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, delimiter=";", encoding="iso-8859-1")

    df.columns = df.columns.str.strip().str.lower()
    df = df.map(lambda s: s.lower().strip() if isinstance(s, str) else s)

    df["data_preco"] = pd.to_datetime(df["data_preco"])
    df["preco_diario"] = pd.to_numeric(df["preco_diario"], errors="coerce")

    df = df.dropna(subset=["dsc_produto", "preco_diario"]).reset_index(drop=True)

    return df


async def get_today_prices(filepath: str) -> pd.DataFrame:
    tz = ZoneInfo(env.TIMEZONE)
    today = datetime.now(tz).date()

    df = await get_data_frame_from_csv(filepath)
    df["date_only"] = df["data_preco"].dt.date

    df_today = df[df["date_only"] == today].copy()

    return df_today


async def get_products_names() -> dict:
    df_daily = await get_data_frame_from_csv(get_today_filename())
    df_monthly = await get_data_frame_from_csv(get_month_filename())

    daily_products = df_daily[["dsc_produto"]].drop_duplicates().reset_index(drop=True)
    daily_products["price_frequency"] = PriceFrequency.DAILY

    monthly_products = (
        df_monthly[["dsc_produto"]].drop_duplicates().reset_index(drop=True)
    )
    monthly_products["price_frequency"] = PriceFrequency.MONTHLY

    result = (
        pd.concat([daily_products, monthly_products])
        .drop_duplicates()
        .reset_index(drop=True)
        .to_dict(orient="records")
    )

    return result
