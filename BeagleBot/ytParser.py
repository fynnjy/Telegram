from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests


def get_youtube_info(link):
    user = UserAgent().random
    headers = {'user-agent': user}

    response = requests.get(link,
                            headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    if '__lang__' in str(soup):
        lang = str(soup)[str(soup).rfind('__lang__'):
                         str(soup).rfind('__lang__') + 14].split('"')[2]
    else:
        lang = 'error'

    if lang == 'en':
        sub = str(soup)[str(soup).rfind('subscribers') - 20:
                        str(soup).rfind('subscribers')].split('"')[-1]

        if 'M' in sub or 'Million' in sub:
            return sub[:-2] + 'M'

        elif 'K' in sub:
            return sub[:-2] + 'K'

    elif lang == 'nl':
        sub = str(soup)[str(soup).rfind('abonnees') - 20:
                        str(soup).rfind('abonnees')].split('"')[-1]

        if 'mln.' in sub or 'miljoen' in sub:
            return sub[:sub.find('mln.')] + 'M'

        else:
            return sub[:-2] + 'K'

    elif lang == 'uk':
        sub = str(soup)[str(soup).rfind('Підписалося'):
                        (str(soup).rfind('користувачів'))
                        + len('користувачів')]

        subscribers_unit_measure = sub[17:20]
        subscribers_count = sub[sub.find('Підписалося')
                                + len('Підписалося') + 1:sub.find(subscribers_unit_measure) - 1]

        return f'{subscribers_count} {subscribers_unit_measure}'

    else:
        return 'non-existent'
