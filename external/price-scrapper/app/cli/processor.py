import io

import pandas as pd

CSV_COLUMNS = [
    "produto",
    "classificao_produto",
    "id_produto",
    "nom_municipio",
    "cod_ibge",
    "uf",
    "regiao",
    "ano",
    "mes",
    "data_inicial_final_semana",
    "semana",
    "dsc_nivel_comercializacao",
    "valor_produto_kg",
]

CSV_TO_DB_MAPPING = {
    "produto": "product",
    "classificao_produto": "classification",
    "id_produto": "product_id",
    "nom_municipio": "municipality",
    "cod_ibge": "ibge_code",
    "uf": "state",
    "regiao": "region",
    "ano": "year",
    "mes": "month",
    "data_inicial_final_semana": "week_date_range",
    "semana": "week_number",
    "dsc_nivel_comercializacao": "commercial_level",
    "valor_produto_kg": "price_per_kg",
}


class CsvProcessorException(Exception):
    pass


def parse_csv_data(csv_data: str) -> pd.DataFrame:
    try:
        string_buffer = io.StringIO(csv_data)
        df = pd.read_csv(string_buffer, sep=";")

        df = df.rename(columns=CSV_TO_DB_MAPPING)

        for col in df.columns:
            df[col] = df[col].str.strip()

        return df
    except Exception as e:
        raise CsvProcessorException(f"Error parsing CSV data: {e}")


def format_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        if "price_per_kg" in df.columns:
            df["price_per_kg"] = (
                df["price_per_kg"].astype(str).str.replace(",", ".").astype(float)
            )

        int_columns = ["product_id", "year", "month", "week_number"]
        for col in int_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

        critical_cols = ["product_id", "municipality", "week_date_range"]
        df = df.dropna(subset=critical_cols)

        return df
    except Exception as e:
        raise CsvProcessorException(f"Error formatting data: {e}")


def process_csv_data(csv_data: str) -> pd.DataFrame:
    df = parse_csv_data(csv_data)
    df = format_data(df)
    return df
