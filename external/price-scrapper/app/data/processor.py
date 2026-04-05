import app.data.csv as csv


def process_csv_data() -> None:
    try:
        csv_data = csv.get_csv_file_data()
    except Exception as e:
        print(f"Error processing CSV data: {e}")
