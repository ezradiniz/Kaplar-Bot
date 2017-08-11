from discord.ext import commands
import json

PLUGINS = [
    'cogs.tibia',
    'cogs.tibiawiki'
]


class Kaplar(commands.Bot):

    def __init__(self, prefix):
        super().__init__(command_prefix=prefix)
        self._load_extensions()

    async def on_ready(self):
        print('Logged in as {}'.format(self.user.name))
        print('------------------------------------------')

    async def on_message(self, message):
        try:
            await self.process_commands(message)
        except Exception as e:
            print(e)

    def _load_extensions(self):
        for cog in PLUGINS:
            try:
                self.load_extension(cog)
                print('Plugin {} loaded successfully'.format(cog))
            except Exception as e:
                print('Failed to load extension {} - Erro: {}'.format(cog, e))


def load_token(file):
    with open(file) as f:
        return json.load(f)


if __name__ == '__main__':
    command_prefix = '!'
    bot = Kaplar(command_prefix)

    try:
        token = load_token('token.json')
        bot.run(token['token'])
    except Exception as e:
        print('Error: {}'.format(e))

