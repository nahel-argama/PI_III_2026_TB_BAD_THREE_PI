import time
from datetime import date
from pathlib import Path

from app.database import con
from app.cli import processor
from app.cli import csv


def ingest_csv(file_path: str) -> dict:
    start_time = time.time()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            csv_data = f.read()
    except Exception as e:
        raise processor.CsvProcessorException(f"Failed to read file {file_path}: {e}")

    processor.validate_structure(csv_data)
    df = processor.process_csv_data(csv_data)

    total_rows = len(df)
    filename = Path(file_path).name

    conn = con.get_db()

    try:
        temp_table = "temp_prices_import"
        conn.register(temp_table, df)

        duplicate_rows = conn.execute(
            f"""
            SELECT COUNT(*) FROM {temp_table}
            WHERE (product_id, municipality, week_date_range) IN (
                SELECT product_id, municipality, week_date_range FROM prices
            )
            """
        ).fetchone()[0]

        conn.execute(
            f"""
            INSERT INTO prices
            SELECT * FROM {temp_table}
            WHERE (product_id, municipality, week_date_range) NOT IN (
                SELECT product_id, municipality, week_date_range FROM prices
            )
            """
        )

        new_rows = total_rows - duplicate_rows

        duration = time.time() - start_time
        con.log_ingestion(conn, filename, total_rows, new_rows, duration)

        conn.execute(f"DROP TABLE IF EXISTS {temp_table}")

        return {
            "filename": filename,
            "total_rows": total_rows,
            "new_rows_inserted": new_rows,
            "duplicate_rows_skipped": duplicate_rows,
            "duration_seconds": duration,
        }

    except Exception as e:
        raise processor.CsvProcessorException(
            f"Error during ingestion of {file_path}: {e}"
        )


def get_csv_filepaths_to_ingest() -> list[str]:
    try:
        current_week_csv = csv.get_csv_current_week_path()
        all_boundaries = csv.get_stored_csv_files_date_boundaries()

        current_week_boundaries = csv.get_csv_date_boundaries(current_week_csv)
    except:


def get_last_ingested_date() -> date:
    try:
        conn = con.get_db()
        result = conn.execute("SELECT MAX(read_date) FROM read_history").fetchone()

        return result[0] if result and result[0] else None
    except Exception as e:
        raise processor.CsvProcessorException(
            f"Error retrieving last ingestion date: {e}"
        )


def ingest_all_pending() -> dict:
    start_time = time.time()
    summary = {
        "files_ingested": 0,
        "total_new_rows": 0,
        "total_duplicates": 0,
        "ingestion_details": [],
        "total_duration_seconds": 0,
    }

    files_to_ingest = get_csv_filepaths_to_ingest()

    for file_path in files_to_ingest:
        try:
            result = ingest_csv(file_path)
            summary["files_ingested"] += 1
            summary["total_new_rows"] += result["new_rows_inserted"]
            summary["total_duplicates"] += result["duplicate_rows_skipped"]
            summary["ingestion_details"].append(result)

            print(
                f"✓ Ingested {file_path}: {result['new_rows_inserted']} new rows "
                f"({result['duplicate_rows_skipped']} duplicates)"
            )

        except processor.CsvProcessorException as e:
            print(f"✗ Error ingesting {file_path}: {e}")
            summary["ingestion_details"].append(
                {"filename": Path(file_path).name, "error": str(e)}
            )

    summary["total_duration_seconds"] = time.time() - start_time
    return summary
