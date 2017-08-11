from discord.ext import commands
from scraper import tibia_scraping
from util import embed, filter
import time


def get_name(*name):
    return ' '.join(name)


class Tibia(object):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def tibia(self, context):
        if context.invoked_subcommand is None:
            await self.bot.say('Invalid tibia command passed...')

    @tibia.command(name='character', aliases=['char'])
    async def _char(self, *character_name):
        name = get_name(*character_name)
        character = tibia_scraping.character(name)
        url = '{}'.format(filter.url_filter_tibia(tibia_scraping.CHARACTER_URL, name))
        em = embed.embed_template(title='Character Information', url=url)
        for key in character['Character Information']:
            em.add_field(name=key, value=character['Character Information'][key])
        if len(character['Character Information']) == 0:
            em.add_field(name='Kaplar !', value='Character not exist')
        await self.bot.say(embed=em)

    @tibia.command(name='death')
    async def _death(self, *character_name):
        name = get_name(*character_name)
        deaths = tibia_scraping.character_key('Character Deaths', name)
        url = '{}'.format(filter.url_filter_tibia(tibia_scraping.CHARACTER_URL, name))
        em = embed.embed_template(title='Character Deaths', url=url)
        if 'Error' in deaths:
            em.add_field(name="Kaplar !", value='Deaths not found')
        else:
            for i in range(len(deaths)):
                em.add_field(name='Death {}'.format(i + 1), value=deaths[i])
        await self.bot.say(embed=em)

    @tibia.command(name='exiva')
    async def _exiva(self, *character_name):
        name = get_name(*character_name)
        character = tibia_scraping.character_status(name)
        em = embed.embed_template()
        if character['status'] != 'online':
            em.add_field(name='Status', value='A Player with this name is not online or status is private')
        else:
            em.add_field(name='Status', value='{} is currently online'.format(name))
        await self.bot.say(embed=em)

    @tibia.command(name='rashid')
    async def _rashid(self):
        now = time.strftime('%A')
        em = embed.embed_template(title='Rashid Info')
        if now.__eq__('monday'):
            em.add_field(name='Rashid',
                         value='On mondays you can find him in Svargrond, in Danwart`s tavern , south of the temple')
        elif now.__eq__('tuesday'):
            em.add_field(name='Rashid',
                         value='On Tuesdays you can find him in Liberty Bay, in Lyonel`s tavern, west of the depot.')
        elif now.__eq__('wednesday'):
            em.add_field(name='Rashid',
                         value='On Wednesdays you can find him in Port Hope, in Clyde`s tavern, west of the depot.')
        elif now.__eq__('thursday'):
            em.add_field(name='Rashid',
                         value='On Thursdays you can find him in Ankrahmun, in Arito`s tavern, above the post office.')
        elif now.__eq__('friday'):
            em.add_field(name='Rashid',
                         value='On Fridays you can find him in Darashia, in Miraia`s tavern, south of the guildhalls.')
        elif now.__eq__('saturday'):
            em.add_field(name='Rashid',
                         value='On Saturdays you can find him in Edron, in Mirabell`s tavern, above the depot.')
        else:
            em.add_field(name='Rashid', value='On Sundays you can find him in Carlin depot, one floor above.')
        await self.bot.say(embed=em)


def setup(bot):
    bot.add_cog(Tibia(bot))