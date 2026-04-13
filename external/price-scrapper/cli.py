from sys import argv

import app.cli as cli


def get_command_str() -> tuple[str, list[str]]:
    if len(argv) < 2:
        return "help", []

    args = []
    if len(argv) > 2:
        args = argv[2:]

    return argv[1], args


def main():
    try:
        command_str, command_args = get_command_str()
        command = cli.parse_command(command_str)
        command.handler(command_args)
    except cli.CommandNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
