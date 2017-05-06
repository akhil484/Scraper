import requests
from lxml import html


dic = dict()
data = dict()
url = "https://en.wikipedia.org/wiki/2017_in_film#Highest_grossing_films"
session = requests.Session()


def get_scrap(url):
    page = session.get(url)
    return page.text


def parse(url):
    source = get_scrap(url)
    tree = html.fromstring(source)
    return tree


if __name__ == '__main__':
    tree = parse(url)
    tables = tree.xpath('//table[@class = "wikitable"]')
    table = tables[0]
    rows = table.xpath('.//tr//i/a')
    for row in rows:
        name = row.xpath('./text()')[0]
        link = row.xpath('./@href')[0]
        dic[name] = link

    for key in dic:
        url = "https://en.wikipedia.org" + dic[key]
        tree = parse(url)
        table = tree.xpath('//table[contains(@class, "infobox")'
                           ' and contains(@class ,"vevent")]/tr')
        for row in table:
            label = row.xpath('.//th//text()')
            value = row.xpath('.//td//text()')
            if len(label) > 1:
                if label[1] == 'Running time':
                    if value != []:
                        print 'added - ', value[0]
                        data[key] = value[0]

    print data



