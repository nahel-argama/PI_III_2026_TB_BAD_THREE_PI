import sys

import app.cli.csv as csv
from app.database.con import init_db


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

    def handler(self) -> None:
        pass


_COMMAND_REGISTRY = {}


def register_command(cmd_class) -> ICommand:
    cmd_instance = cmd_class()
    _COMMAND_REGISTRY[cmd_instance.command()] = cmd_instance
    return cmd_class


@register_command
class HelpCommand(ICommand):
    def command(self) -> str:
        return "help"

    def title(self) -> str:
        return "Show this help message"

    def help(self) -> str:
        return "Show this help message."

    def handler(self) -> None:
        print("Available commands:\n")

        commands = _COMMAND_REGISTRY.values()

        for cmd in commands:
            title_text = f"{cmd.command()}:"
            help_text = cmd.help()

            print(f"{" "*5}{title_text}")
            print(f"{" "*8}{help_text}\n")


@register_command
class GetCsvCommand(ICommand):
    def command(self) -> str:
        return "get-csv"

    def title(self) -> str:
        return "Download and store price data"

    def help(self) -> str:
        return "Download the price data from the source website and store it locally."

    def handler(self) -> None:
        try:
            csv.download_csv()
        except Exception as e:
            print(f"Error downloading CSV file: {e}", file=sys.stderr)


@register_command
class InitDbCommand(ICommand):
    def command(self) -> str:
        return "init-db"

    def title(self) -> str:
        return "Initialize the database"

    def help(self) -> str:
        return "Create the necessary tables in the database if they don't exist."

    def handler(self) -> None:
        try:
            init_db()
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Error initializing database: {e}", file=sys.stderr)


@register_command
class IngestCommand(ICommand):
    def commnad(self) -> str:
        return "ingest"

    def title(self) -> str:
        return "Ingest CSV data into the database"

    def help(self) -> str:
        return "Read the downloaded CSV file and insert its data into the database."

    def handler(self) -> None:
        try:
            # TODO implementar aqui
            print("CSV data ingested successfully.")
        except Exception as e:
            print(f"Error ingesting CSV data: {e}", file=sys.stderr)


def parse_command(command_str: str) -> ICommand:
    cmd = _COMMAND_REGISTRY.get(command_str)
    if not cmd:
        raise CommandNotFoundError(
            f"Command '{command_str}' not found. Use 'help' to see available commands."
        )
    return cmd
