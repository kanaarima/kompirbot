from typing import Generic, TypeVar, Optional, Type
from enum import IntEnum

import discord

T = TypeVar('T')

class Permission(IntEnum):
    NONE = 0
    SERVER_ADMIN = 1
    BOT_ADMIN = 2

class Argument(Generic[T]):
    
    def __init__(self, required: bool, default_value: Optional[T] = None, position: Optional[int] = None) -> None:
        self.required = required
        self.value = default_value
        self.position = position

    def parse(self, value: str):
        pass

class StringArgument(Argument[str]):
    
    def parse(self, value: str):
        self.value = value

class IntArgument(Argument[int]):
    
    def __init__(self, required: bool, default_value: Optional[int] = None, position: int = -1, min_value: Optional[int] = None, max_value: Optional[int] = None) -> None:
        super().__init__(required, default_value, position)
        self.min_value = min_value
        self.max_value = max_value
    
    def parse(self, value: str):
        self.value = int(value)
        if self.min_value is not None and self.value < self.min_value:
            raise ValueError(f"Value must be at least {self.min_value}")
        if self.max_value is not None and self.value > self.max_value:
            raise ValueError(f"Value must be at most {self.max_value}")

class CommandArguments:

    def __init__(self, message: discord.Message) -> None:
        args = {'positional': list()}
        for x in message.content.split(" ")[1:]:
            if "=" in x:
                key, value = x.split("=", maxsplit=1)
                args[key] = value
            else:
                args['positional'].append(x)
        for name, value in self.__dict__.items():
            if not isinstance(value, Argument):
                 continue
            argument: Argument = value
            if argument.position is not None or argument.position > -1:
                if argument.position >= len(args['positional']):
                    if argument.required:
                        raise ValueError(f"Missing required argument '{name}' of type {type(argument)} at position {argument.position}")
                    else:
                        continue
                else:
                    print(argument.position)
                    argument.parse(args['positional'][argument.position])
            else:
                if name in args:
                    argument.parse(args[name])
                else:
                    if argument.required:
                        raise ValueError(f"Missing required argument '{name}' of type {type(argument)}")

class Command:
    
    def __init__(self, name: str, description: str = "No description provided.", help: str = "No help provided.", permission: Permission = Permission.NONE, parser: Optional[Type[CommandArguments]] = None) -> None:
        self.name = name
        self.description = description
        self.help = help
        self.permission = permission
        self.parser = parser
    
    def add_to_tree(self, tree: discord.app_commands.CommandTree) -> None:
        pass

    async def execute(self, message: discord.Message, args: Optional[CommandArguments] = None) -> None:
        pass