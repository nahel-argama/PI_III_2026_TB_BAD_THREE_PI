import io

import pandas as pd

import app.data.csv as csv


class CsvProcessorException(Exception):
    pass


def process_csv_data() -> None:
    try:
        csv_data = csv.get_csv_file_data()

    except Exception as e:
        print(f"Error processing CSV data: {e}")


def validate_structure(csv_data: str) -> bool:
    string_buffer = io.StringIO(csv_data)

    pg = pd.read_csv(sep=";", filepath_or_buffer=string_buffer)
    pass


def parse_csv_data(csv_data: str):
    pass


def data_difference(data1: str, data2: str):
    pass
