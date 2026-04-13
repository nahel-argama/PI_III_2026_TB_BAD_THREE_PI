import asyncio
import sys

import app.database as db
import app.data as data


class CommandNotFoundError(Exception):
    pass


class ICommand:
    @property
    def command(self) -> str:
        pass

    @property
    def title(self) -> str:
        return ""

    @property
    def help(self) -> str:
        return """"""

    def handler(self, args: list[str]) -> None:
        pass


_COMMAND_REGISTRY = {}


def _register_command(cmd_class) -> ICommand:
    cmd_instance = cmd_class()
    _COMMAND_REGISTRY[cmd_instance.command()] = cmd_instance
    return cmd_class


@_register_command
class HelpCommand(ICommand):
    def command(self) -> str:
        return "help"

    def title(self) -> str:
        return "Show this help message"

    def help(self) -> str:
        return "Show this help message."

    def handler(self, args: list[str]) -> None:
        print("Available commands:\n")

        commands = _COMMAND_REGISTRY.values()

        for cmd in commands:
            title_text = f"{cmd.command()}:"
            help_text = cmd.help()

            print(f"{" "*5}{title_text}")
            print(f"{" "*8}{help_text}\n")


@_register_command
class Migrate(ICommand):
    def command(self) -> str:
        return "migrate"

    def title(self) -> str:
        return "Run database migrations"

    def help(self) -> str:
        return "Create the necessary tables in the database if they don't exist."

    def handler(self, args: list[str]) -> None:
        try:
            db.migrate()
            print("Database migrated successfully.")
        except Exception as e:
            print(f"Error migrating database: {e}", file=sys.stderr)


@_register_command
class CreateMigrationCommand(ICommand):
    def command(self) -> str:
        return "create-migration"

    def title(self) -> str:
        return "Create a new database migration file"

    def help(self) -> str:
        return "Create a new database migration file with the given name."

    def handler(self, args: list[str]) -> None:
        name = ""
        if len(args) > 0:
            name = args[0].strip()

        if not name:
            print("Migration name cannot be empty.", file=sys.stderr)
            return

        try:
            db.create_migration(name)
            print(f"Migration '{name}' created successfully.")
        except Exception as e:
            print(f"Error creating migration: {e}", file=sys.stderr)


@_register_command
class IngestProductsCommand(ICommand):
    def command(self) -> str:
        return "ingest-products"

    def title(self) -> str:
        return "Ingest CONAB products from agrobr"

    def help(self) -> str:
        return "Fetch horticultural products from CONAB via agrobr and store them in the database."

    def handler(self, args: list[str]) -> None:
        try:
            filepath = args[0] if args else data.get_today_filename()

            result = asyncio.run(data.ingest_products(filepath))

            print(f"Products ingested: {result.inserted} inserted.")
        except Exception as e:
            print(f"Error ingesting products: {e}", file=sys.stderr)


@_register_command
class IngestPricesCommand(ICommand):
    def command(self) -> str:
        return "ingest-prices"

    def title(self) -> str:
        return "Ingest daily prices from agrobr"

    def help(self) -> str:
        return "Fetch daily product prices from CONAB via agrobr and store them in the database."

    def handler(self, args: list[str]) -> None:
        try:
            filepath = args[0] if args else data.get_today_filename()
            result = asyncio.run(data.ingest_daily_prices(filepath))
            print(
                f"Prices ingested: {result['inserted']} inserted, {result['skipped']} skipped, {result['total']} total."
            )
        except Exception as e:
            print(f"Error ingesting prices: {e}", file=sys.stderr)


@_register_command
class DownloadDailyCommand(ICommand):
    def command(self) -> str:
        return "download-daily"

    def title(self) -> str:
        return "Download daily CSV data"

    def help(self) -> str:
        return "Download daily product data from PROHORT and save to data directory with current date as filename."

    def handler(self, args: list[str]) -> None:
        try:
            result = asyncio.run(data.download_daily_csv())
            print(f"Daily data downloaded successfully in file: {result}")
        except Exception as e:
            print(f"Error downloading daily data: {e}", file=sys.stderr)


@_register_command
class DownloadMonthlyCommand(ICommand):
    def command(self) -> str:
        return "download-monthly"

    def title(self) -> str:
        return "Download monthly CSV data"

    def help(self) -> str:
        return "Download monthly product data from PROHORT and save to data directory with current month as filename."

    def handler(self, args: list[str]) -> None:
        try:
            result = asyncio.run(data.download_monthly_csv())
            print(f"Monthly data downloaded successfully in file: {result}")
        except Exception as e:
            print(f"Error downloading monthly data: {e}", file=sys.stderr)


@_register_command
class DeleteDataCommand(ICommand):
    def command(self) -> str:
        return "delete-data"

    def title(self) -> str:
        return "Delete data files"

    def help(self) -> str:
        return "Delete data files. Use --all to delete all files, or provide a date (YYYY-MM-DD)."

    def handler(self, args: list[str]) -> None:
        try:
            data.delete_data_dir()
        except Exception as e:
            print(f"Error deleting data: {e}", file=sys.stderr)


def parse_command(command_str: str) -> ICommand:
    cmd = _COMMAND_REGISTRY.get(command_str)
    if not cmd:
        raise CommandNotFoundError(
            f"Command '{command_str}' not found. Use 'help' to see available commands."
        )
    return cmd
