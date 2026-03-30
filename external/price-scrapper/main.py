from app.csv import download_csv


def main():
    print("Starting the CSV download process...")
    result = download_csv()
    print(result)


if __name__ == "__main__":
    main()
