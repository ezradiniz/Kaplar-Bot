
def url_filter_tibia(url, name):
    return url + name.replace(' ', '+')


def url_filter_wiki(url, name):
    if 'of inferno' not in name.lower():
        name = name.replace('_Of_', '_of_')
    return url + name.replace(' ', '_')


def text_filter(text):
    return text.strip().replace('\xa0', ' ')