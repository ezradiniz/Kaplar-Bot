from discord.ext import commands
from scraper import tibia_scraping
from util import embed, filter


class Tibiawiki(object):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def wiki(self, context):
        if context.invoked_subcommand is None:
            await self.bot.say('Invalid wiki command passed...')

    @wiki.command(name='item')
    async def _item(self, *item):
        item = ' '.join(item)
        res = tibia_scraping.item(item)
        url = '{}'.format(filter.url_filter_wiki(tibia_scraping.WIKI_URL, item.title()))
        em = embed.embed_template(title='Tibia Wiki', url=url)
        if len(res['item']) == 0:
            em.add_field(name='Kaplar', value='Item not found')
        else:
            em.set_image(url=res['image']['url'])
            for key in res['item']:
                em.add_field(name=key, value=res['item'][key])
        await self.bot.say(embed=em)

    @wiki.command(name='monster')
    async def _monster(self, *monster):
        monster = ' '.join(monster)
        res = tibia_scraping.monster(monster)
        try:
            url = '{}'.format(filter.url_filter_wiki(tibia_scraping.WIKI_URL, monster.title()))
            em = embed.embed_template(title='Monster Wiki', url=url)
            if len(res['image']) != 0:
                em.set_image(url=res['image']['url'])
            if len(res['monster']) == 0:
                em.add_field(name='Kaplar', value='Monster not found')
            else:
                for key in res['monster']:
                    if res['monster'][key] != '' and key != '':
                        em.add_field(name=key, value=res['monster'][key])
        except Exception as e:
            print('Exception monster {}'.format(e))
        await self.bot.say(embed=em)

    @wiki.command(name='loot')
    async def _loot(self, *monster):
        monster = ' '.join(monster)
        res = tibia_scraping.loot(monster)
        try:
            url = '{}'.format(filter.url_filter_wiki(tibia_scraping.WIKI_URL, monster.title()))
            em = embed.embed_template(title='Loot Wiki', url=url)
            if len(res) == 0:
                em.add_field(name='Kaplar', value='Monster not found')
            else:
                item = ''
                size = len(res['Loot'])
                for i in range(size):
                    item += res['Loot'][i] + '\n'
                    if i > 0 and i % 30 == 0:
                        em.add_field(name='Loot', value=item)
                        item = ''
                    if i == size - 1:
                        em.add_field(name='Loot', value=item)
        except Exception as e:
            print('Exception loot {}'.format(e))
        await self.bot.say(embed=em)


def setup(bot):
    bot.add_cog(Tibiawiki(bot))
