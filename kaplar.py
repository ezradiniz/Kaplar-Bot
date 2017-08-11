from discord.ext import commands
import json

EXTENSIONS = [
    'extensions.tibia',
    'extensions.tibiawiki'
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
        for ext in EXTENSIONS:
            try:
                self.load_extension(ext)
                print('Extension {} loaded successfully'.format(ext))
            except Exception as e:
                print('Failed to load extension {} - Erro: {}'.format(ext, e))


def load_token(file):
    with open(file) as f:
        return json.load(f)


if __name__ == '__main__':
    command_prefix = '!'
    bot = Kaplar(command_prefix)

    try:
        token = load_token('YOUR TOKEN HERE !')
        bot.run(token['token'])
    except Exception as e:
        print('Error: {}'.format(e))

