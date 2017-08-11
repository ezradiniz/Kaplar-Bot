from discord.ext import commands

class Tibia(object):

    def __init__(self, bot):
    self.bot = bot

    @commands.group(pass_context=True)
    async def tibia(self, context):
        if context.invoked_subcommand is None:
            await self.bot.say('Invalid tibia command passed...')


def setup(bot):
    bot.add_cog(Tibia(bot))