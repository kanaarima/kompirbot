import app.discord.commands
import discord
import config

class DiscordClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.tree = discord.app_commands.CommandTree(self)
        await self.tree.sync() # should change this at some point

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.content.startswith('?'):
            for x in app.discord.commands.all:
                if x.name == message.content[1:].split()[0]:
                    arguments = None
                    if x.parser:
                        try:
                            arguments = x.parser(message)
                        except ValueError as e:
                            await message.reply(f"Error parsing arguments!!! ```{repr(e)}```")
                            break
                    await x.execute(message, arguments)
                    break

def main():
    client = DiscordClient(intents = discord.Intents.all())
    client.run(config.DISCORD_TOKEN)
