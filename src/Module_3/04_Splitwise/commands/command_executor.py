class CommandExecutor:
    def __init__(self, commands):
        self.commands = commands

    def execute_command(self, input_str: str) -> None:
        for command in self.commands:
            if command.matches(input_str):
                command.execute(input_str)
                return
        print("Invalid command.")