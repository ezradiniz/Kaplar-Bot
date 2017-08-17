import urllib.request as req
from bs4 import BeautifulSoup as bs
from util import utils

CHARACTER_URL = 'https://secure.tibia.com/community/?name='
WIKI_URL= 'http://tibia.wikia.com/wiki/'
WORLD_URL = 'https://secure.tibia.com/community/?subtopic=worlds&world='


def character(character_name):
    request_url = utils.url_filter_tibia(CHARACTER_URL, character_name)
    content = req.urlopen(request_url).read()
    tables = bs(content, 'lxml').select('.BoxContent')[0].find_all('table')
    response = {
        'Character Information': {},
        'Account Achievements': [],
        'Character Deaths': [],
        'Account Information': {}
    }
    for table in tables:
        table_name = table.tr.get_text()
        trs = table.findAll('tr')
        if table_name == 'Character Information' or table_name == 'Account Information':
            for tr in trs:
                text = utils.text_filter(tr.get_text())
                if text != table_name:
                    key_value = text.split(':')
                    if key_value[1].strip() != '':
                        response[table_name][key_value[0]] = key_value[1]
        elif table_name == 'Account Achievements' or table_name == 'Character Deaths':
            for tr in trs:
                text = utils.text_filter(tr.get_text())
                if text != table_name:
                    response[table_name].append(text)
    return response


def character_key(key, character_name):
    try:
        return character(character_name)[key]
    except Exception as e:
        return {'Error': 'Key not found'}


def world(world_name):
    response = {}
    try:
        request_url = utils.url_filter_tibia(WORLD_URL, world_name.title())
        content = req.urlopen(request_url).read()
        tables = bs(content, 'lxml').find_all('div', lass_='InnerTableContainer')[1].table
        rows = tables.find_all('tr', recursive=False)
        for row in rows:
            cols = row.find_all('td')
            key = cols[0].get_text()
            value = cols[1].get_text()
            response[key] = value
    except Exception as e:
        print('Error World: {}'.format(e))
    return response


def character_status(character_name):
    request_url = utils.url_filter_tibia(CHARACTER_URL, character_name)
    content = req.urlopen(request_url).read()
    tables = bs(content, 'lxml').select('.BoxContent')[0].find_all('table')
    response = {
        'status': 'undefined'
    }
    character_name = character_name.lower()
    for i in range(len(tables), 0, -1):
        try:
            for t in tables[i].select('.green'):
                char_name = utils.text_filter(t.parent.parent.td.get_text().lower()).split('.')[1].strip()
                if char_name == character_name:
                    response['status'] = 'online'
                    return response
        except Exception as e:
            pass
    return response


def loot(loot_name):
    request_url = utils.url_filter_tibia(WIKI_URL, loot_name.title())
    response = {}
    try:
        content = req.urlopen(request_url).read()
        loot = bs(content, 'lxml').find(id='loot_perc_loot')
        response['Loot'] = loot.get_text().split('\n')
    except Exception as e:
        pass
    return response


def item(item_name):
    request_url = utils.url_filter_wiki(WIKI_URL, item_name.title())
    response = {
        'item': {},
        'image': {}
    }
    try:
        content = req.urlopen(request_url).read()
        scraping = bs(content, 'lxml')
        header = scraping.select('.item-look')[0].get_text()
        note = scraping.find(id='item-notes').p
        url = scraping.find(id='twbox-image').a['href']

        response['item']['Name'] = header
        response['image']['url'] = url
        if note is not None:
            response['item']['Note'] = note.get_text()
        infobox = scraping.find('table', class_='infobox')
        rows = infobox.find_all('tr', recursive=False)

        for tr in rows:
            key = tr.find(class_='property')
            value = tr.find(class_='value')
            if key is None or value is None: continue
            response['item'][key.get_text()] = value.get_text()
    except Exception as e:
        print('Item {}'.format(e))
    return response


def monster(monster_name):
    request_url = utils.url_filter_wiki(WIKI_URL, monster_name.title())
    response = {
        'monster': {},
        'image': {}
    }
    try:
        content = req.urlopen(request_url).read()
        scraping = bs(content, 'lxml')
        table = scraping.find(id='tabular-data').table
        note = scraping.find('blockquote')
        url = scraping.find(id='twbox-image').a['href']
        response['monster']['Name'] = monster_name
        response['image']['url'] = url

        # if has note
        if note is not None:
            response['monster']['Note'] = note.get_text()

        rows = table.find_all('tr', recursive=False)
        for tr in rows:
            key = tr.find(class_='property')
            value = tr.find(class_='value')
            if key is None or value is None: continue
            response['monster'][key.get_text()] = value.get_text()
    except Exception as e:
        print('Monster {}'.format(e))
    return response

