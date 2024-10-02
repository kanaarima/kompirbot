from app.discord.objects import Command, CommandArguments, IntArgument
from discord import Message

class PingArguments(CommandArguments):
    
    def __init__(self, message: Message) -> None:
        self.repeat = IntArgument(required=False, position=0, default_value=1, min_value=1, max_value=10)
        super().__init__(message)

class Ping(Command):

    def __init__(self) -> None:
        super().__init__('ping', parser=PingArguments)

    async def execute(self, message: Message, args: PingArguments) -> None:
        for x in range(args.repeat.value):
            await message.reply(f'Pong! {x}')
