from lxml import html
import requests
from datetime import date
page = requests.get('https://tudonumclick.com/programacao-tv/mais-canais/')
tree = html.fromstring(page.content)
hrefs = tree.xpath('.//a[@class="htdn"]')

for href in hrefs:
    print href.attrib['href']
