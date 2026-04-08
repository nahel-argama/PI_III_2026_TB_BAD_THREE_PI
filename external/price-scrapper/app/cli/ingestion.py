import time
from datetime import date
from pathlib import Path

from app.database import con
from app.cli import processor
from app.cli import csv

def get_csv_filepaths_to_ingest() -> list[str]:
    try:
        current_week_csv = csv.get_csv_current_week_path()
        all_boundaries = csv.get_stored_csv_files_date_boundaries()

        current_week_boundaries = csv.get_csv_date_boundaries(current_week_csv)
    except:
