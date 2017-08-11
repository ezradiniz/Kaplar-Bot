from discord.ext import commands

class Tibiawiki(object):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def wiki(self, context):
        if context.invoked_subcommand is None:
            await self.bot.say('Invalid wiki command passed...')


def setup(bot):
    bot.add_cog(Tibiawiki(bot))