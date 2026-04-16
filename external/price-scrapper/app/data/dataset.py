from datetime import datetime
from typing import TypedDict
from zoneinfo import ZoneInfo

import pandas as pd

from app import env
from app.database.products import PriceFrequency


class ProductNameContract(TypedDict):
    name: str
    price_frequency: str


def _normalize_frame(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower()
    df = df.map(lambda s: s.lower().strip() if isinstance(s, str) else s)
    return df


def _parse_month_decimal(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False),
        errors="coerce",
    )


def _build_products_names_contract(
    df: pd.DataFrame, price_frequency: str
) -> list[ProductNameContract]:
    products = df[["dsc_produto"]].drop_duplicates().reset_index(drop=True)
    products["price_frequency"] = price_frequency
    products = products.rename(columns={"dsc_produto": "name"})

    return products[["name", "price_frequency"]].to_dict(orient="records")


async def get_daily_data_frame_from_csv(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, delimiter=";", encoding="iso-8859-1")

    df = _normalize_frame(df)

    df["data_preco"] = pd.to_datetime(df["data_preco"])
    df["preco_diario"] = pd.to_numeric(df["preco_diario"], errors="coerce")

    df = df.dropna(subset=["dsc_produto", "preco_diario"]).reset_index(drop=True)

    return df


async def get_month_data_frame_from_csv(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, delimiter=";", encoding="iso-8859-1")

    df = _normalize_frame(df)

    df["qtd_comercializada_kg"] = _parse_month_decimal(df["qtd_comercializada_kg"])
    df["valor_comercializado"] = _parse_month_decimal(df["valor_comercializado"])

    df["id_ano_comercializacao"] = pd.to_numeric(
        df["id_ano_comercializacao"], errors="coerce"
    )
    df["id_mes_comercializacao"] = pd.to_numeric(
        df["id_mes_comercializacao"], errors="coerce"
    )

    df["data_preco"] = pd.to_datetime(
        {
            "year": df["id_ano_comercializacao"],
            "month": df["id_mes_comercializacao"],
            "day": 1,
        },
        errors="coerce",
    )

    df["preco_mensal"] = df["valor_comercializado"] / df["qtd_comercializada_kg"]
    df["preco_mensal"] = pd.to_numeric(df["preco_mensal"], errors="coerce")

    df = df.dropna(subset=["dsc_produto", "data_preco"]).reset_index(drop=True)

    return df


async def get_today_prices(filepath: str) -> pd.DataFrame:
    tz = ZoneInfo(env.TIMEZONE)
    today = datetime.now(tz).date()

    df = await get_daily_data_frame_from_csv(filepath)
    df["date_only"] = df["data_preco"].dt.date

    df_today = df[df["date_only"] == today].copy()

    return df_today


async def get_daily_products_names(filepath: str) -> list[ProductNameContract]:
    df = await get_daily_data_frame_from_csv(filepath)
    return _build_products_names_contract(df, PriceFrequency.DAILY)


async def get_monthly_products_names(filepath: str) -> list[ProductNameContract]:
    df = await get_month_data_frame_from_csv(filepath)
    return _build_products_names_contract(df, PriceFrequency.MONTHLY)


async def get_products_names_merged(
    daily_filepath: str, monthly_filepath: str
) -> list[ProductNameContract]:
    daily_products = await get_daily_products_names(daily_filepath)
    monthly_products = await get_monthly_products_names(monthly_filepath)

    daily_names = {p["name"] for p in daily_products}
    monthly_names = {p["name"] for p in monthly_products}

    shared_names = daily_names & monthly_names
    daily_only_names = daily_names - monthly_names
    monthly_only_names = monthly_names - daily_names

    merged_products: list[ProductNameContract] = []

    for name in sorted(shared_names):
        merged_products.append({"name": name, "price_frequency": PriceFrequency.BOTH})

    for name in sorted(daily_only_names):
        merged_products.append({"name": name, "price_frequency": PriceFrequency.DAILY})

    for name in sorted(monthly_only_names):
        merged_products.append({"name": name, "price_frequency": PriceFrequency.MONTHLY})

    return merged_products
