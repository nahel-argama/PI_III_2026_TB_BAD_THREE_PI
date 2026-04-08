from sys import argv

import app.cli.command as cmd


def get_command_str() -> str:
    if len(argv) < 2:
        return "help"

    if len(argv) > 2:
        print("Warning: More than one argument provided.")
        return "help"

    return argv[1]


def main():
    try:
        command_str = get_command_str()
        command = cmd.parse_command(command_str)
        command.handler()
    except cmd.CommandNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
