from discord import Embed

KAPLAR_THUMBNAIL_IMG = 'http://www.tibiawiki.com.br/images/9/95/Minotaur.gif'


def embed_template(**kwargs):
    if 'colour' not in kwargs:
        kwargs['colour'] = 0xF47D42
    embed = Embed(**kwargs)
    embed.set_thumbnail(url=KAPLAR_THUMBNAIL_IMG)
    return embed