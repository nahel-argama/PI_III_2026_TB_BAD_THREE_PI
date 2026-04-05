import sys

import app.data.processor as processor
import app.data.csv as csv


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


def register_command(cmd_class):
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

    def handler(self):
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

    def handler(self):
        try:
            csv.download_csv()
        except Exception as e:
            print(f"Error downloading CSV file: {e}", file=sys.stderr)


@register_command
class ProcessCsvCommand(ICommand):
    def command(self) -> str:
        return "process-csv"

    def title(self) -> str:
        return "Process price data"

    def help(self) -> str:
        return "Process and store the price data in the database. If the data is not downloaded, it will be downloaded first."

    def handler(self):
        try:
            processor.process_csv_data()
        except Exception as e:
            print(f"Error processing CSV data: {e}", file=sys.stderr)


def parse_command(command_str: str) -> ICommand:
    cmd = _COMMAND_REGISTRY.get(command_str)
    if not cmd:
        raise CommandNotFoundError(
            f"Command '{command_str}' not found. Use 'help' to see available commands."
        )
    return cmd
