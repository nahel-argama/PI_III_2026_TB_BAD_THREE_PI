from app.cli.csv import get_stored_csv_files_date_boundaries


def main():
    stored = get_stored_csv_files_date_boundaries()
    print(stored)


if __name__ == "__main__":
    main()
