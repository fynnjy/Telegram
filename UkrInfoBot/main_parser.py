from bs4 import BeautifulSoup
import requests
import json


# Новости с Униан
def news_unian():
    response = requests.get('https://www.unian.net/detail/all_news')
    soup = BeautifulSoup(response.text, 'lxml')
    newsBlocks = soup.find_all('div', class_='list-thumbs__item')

    news_dict = {}
    for infoBlock in range(len(newsBlocks)):
        infoNews = newsBlocks[infoBlock].find('div', class_='list-thumbs__info').find('a')
        timeNews = newsBlocks[infoBlock].find('div', class_='list-thumbs__time time').text.strip()
        linkNews = infoNews.get("href")

        # ID из ссылки
        news_id = linkNews.split('-')[-1]
        news_id = news_id[:-5]

        # ID из времени
        '''news_id = timeNews.replace(':', '')
        news_id = news_id.replace(', ', '')
        news_id = news_id.replace('.', '')'''

        news_dict[news_id] = {
            "news_time": timeNews,
            "news_title": infoNews.text.strip(),
            "news_url": linkNews,
            "ulr_title": 'Открыть статью на сайте 👁️‍'
        }

    with open('dicts/newsUnian.json', 'w', encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


# Обновление новостей на Униан
def updates_unian():
    with open('dicts/newsUnian.json', encoding="utf-8") as file:
        news_dict = json.load(file)

    response = requests.get('https://www.unian.net/detail/all_news')
    soup = BeautifulSoup(response.text, 'lxml')
    newsBlocks = soup.find_all('div', class_='list-thumbs__item')

    fresh_news = {}
    for infoBlock in range(len(newsBlocks)):
        infoNews = newsBlocks[infoBlock].find('div', class_='list-thumbs__info').find('a')
        linkNews = infoNews.get("href")

        # ID из ссылки
        news_id = linkNews.split('-')[-1]
        news_id = news_id[:-5]

        # ID из времени
        '''news_id = timeNews.replace(':', '')
        news_id = news_id.replace(', ', '')
        news_id = news_id.replace('.', '')'''

        if news_id in news_dict:
            continue
        else:
            timeNews = newsBlocks[infoBlock].find('div', class_='list-thumbs__time time').text.strip()

            news_dict[news_id] = {
                "news_time": timeNews,
                "news_title": infoNews.text.strip(),
                "news_url": linkNews,
                "ulr_title": 'Открыть статью на сайте 👁️‍'
            }

            fresh_news[news_id] = {
                "news_time": timeNews,
                "news_title": infoNews.text.strip(),
                "news_url": linkNews,
                "ulr_title": 'Открыть статью на сайте 👁️‍'
            }

    with open("dicts/newsUnian.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


# Получение новостей с РБК
def news_rbc():
    rbc_news = requests.get('https://www.rbc.ua/ukr/news')
    soup = BeautifulSoup(rbc_news.text, 'lxml')
    mainBlock = soup.find('div', class_='newsline')
    newsBlocks = mainBlock.find_all('div', class_='')

    rbcNews_dict = {}
    for sequence in range(len(newsBlocks)):
        newsLink = newsBlocks[sequence].find('a').get('href')
        newsTitle = newsBlocks[sequence].find('a').text.strip()
        newsTitle = newsTitle[6:]

        newsTime = newsBlocks[sequence].find('span', class_='time').text.strip()

        # ID из ссылки
        news_id = newsLink.split('-')[-1]
        news_id = news_id.split('.')[0]

        # ID из времени
        '''news_id = newsTime.replace(':', '')'''

        rbcNews_dict[news_id] = {
            'news_time': newsTime,
            'news_title': newsTitle,
            'news_link': newsLink
        }

    with open('dicts/newsRbc.json', 'w', encoding="utf-8") as file:
        json.dump(rbcNews_dict, file, indent=4, ensure_ascii=False)


# Обновление новостей на РБК
def updates_rbc():
    with open('dicts/newsRbc.json', encoding="utf-8") as file:
        rbcNews_dict = json.load(file)

        rbc_news = requests.get('https://www.rbc.ua/ukr/news')
        soup = BeautifulSoup(rbc_news.text, 'lxml')
        mainBlock = soup.find('div', class_='newsline')
        newsBlocks = mainBlock.find_all('div', class_='')

        freshNews = {}
        for sequence in range(len(newsBlocks)):
            newsLink = newsBlocks[sequence].find('a').get('href')

            # ID из ссылки
            news_id = newsLink.split('-')[-1]
            news_id = news_id.split('.')[0]

            # ID из времени
            '''news_id = newsTime.replace(':', '')'''

            if news_id in rbcNews_dict:
                continue
            else:
                newsTime = newsBlocks[sequence].find('span', class_='time').text.strip()
                newsTitle = newsBlocks[sequence].find('a').text.strip()
                newsTitle = newsTitle[6:]

                rbcNews_dict[news_id] = {
                    'news_time': newsTime,
                    'news_title': newsTitle,
                    'news_link': newsLink
                }

                freshNews[news_id] = {
                    'news_time': newsTime,
                    'news_title': newsTitle,
                    'news_link': newsLink
                }

        with open('dicts/newsRbc.json', 'w', encoding="utf-8") as file:
            json.dump(rbcNews_dict, file, indent=4, ensure_ascii=False)

        return freshNews


# Получение новостей из BBC
def news_bbc():
    bbc = requests.get("https://www.bbc.com/russian/topics/cez0n29ggrdt")
    soup = BeautifulSoup(bbc.text, "lxml")
    all_news = soup.find_all("div", class_="bbc-bjn8wh e1v051r10")

    news_dict = {}
    for news in all_news:
        news_date = news.find("time", class_="bbc-16jlylf e1mklfmt0").text.strip()
        news_title = news.find("a", class_="bbc-uk8dsi e1d658bg0").text.strip()
        news_link = news.find("a").get("href")

        news_id = news_link.split("-")[-1]

        news_dict[news_id] = {
            "news_time": news_date,
            "news_title": news_title,
            "news_url": news_link
        }

    with open("dicts/newsBBC.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


# Обновление новостей из BBC
def updates_bbc():
    with open("dicts/newsBBC.json", encoding="utf-8") as file:
        news_dict = json.load(file)

    bbc = requests.get("https://www.bbc.com/russian/topics/cez0n29ggrdt")
    soup = BeautifulSoup(bbc.text, "lxml")
    all_news = soup.find_all("div", class_="bbc-bjn8wh e1v051r10")

    fresh_news = {}
    for news in all_news:
        news_link = news.find("a").get("href")
        news_id = news_link.split("-")[-1]

        if news_id in news_dict:
            continue
        else:
            news_date = news.find("time", class_="bbc-16jlylf e1mklfmt0").text.strip()
            news_title = news.find("a", class_="bbc-uk8dsi e1d658bg0").text.strip()
            news_link = news.find("a").get("href")

            news_dict[news_id] = {
                "news_time": news_date,
                "news_title": news_title,
                "news_url": news_link
            }

            fresh_news[news_id] = {
                "news_time": news_date,
                "news_title": news_title,
                "news_url": news_link
            }

    with open("dicts/newsBBC.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


# Курсы валют
def get_currency():
    privat = requests.get('https://finance.ua/banks/privatbank/currency')
    soup = BeautifulSoup(privat.text, 'lxml')
    currencyBlock = soup.find('tbody', class_='sc-tu3zio-4 lgYGob')

    tr = currencyBlock.find_all('tr', class_='sc-tu3zio-6 dxVZUp')
    currency_dict = {}
    for currency in range(len(tr)):
        td_cur = tr[currency].find('td', class_='sc-tu3zio-1 bkzMqb').text.strip()
        td = tr[currency].find('td', class_='sc-tu3zio-5 JpgSG').text.strip()
        value = td[:-6].replace('-', '')
        td = tr[currency].find_all('td')
        for value_sale in td:
            sale_1 = value_sale.text.replace(td_cur, '')
            sale_2 = sale_1.replace(value, '')
            sale_3 = sale_2.replace('-', '')
            sale = sale_3[:-6]

            currency_dict[td_cur] = {
                'currency_name': td_cur,
                'currency_buy': value,
                'currency_sale': sale
            }

    with open('dicts/currency_dict.json', 'w', encoding="utf-8") as currency_file:
        json.dump(currency_dict, currency_file, indent=4, ensure_ascii=False)
