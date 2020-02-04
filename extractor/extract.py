from lxml import html
import lxml.etree
import lxml.builder
import requests
from datetime import date
from datetime import datetime
from datetime import timedelta
import cgi
E = lxml.builder.ElementMaker()
ROOT = E.programme
DOC = E.doc
FIELD1 = E.field1
FIELD2 = E.field2
FIELD3 = E.field3
FIELD4 = E.field4

file = open("guide.xml","w") 


list_channel = requests.get('https://tudonumclick.com/programacao-tv/mais-canais/')
tree1 = html.fromstring(list_channel.content)
hrefs = tree1.xpath('.//a[@class="htdn"]')
today = date.today()
d1 = today.strftime("%Y%m%d")
print datetime.today().strftime('%A')
weekDays = ('segunda','terca','quarta','quinta','sexta','sabado','domingo')
for i in range(0, 6):
 d2 = today + timedelta(days=i)
 print d2.strftime("%Y%m%d")
 print weekDays[d2.weekday()]
#exit()
file.write('<?xml version="1.0" encoding="UTF-8"?>')
#file.write('<tv generator-info-name="WebGrab+Plus/w MDB &amp; REX Postprocess -- version  V2.1 -- Jan van Straaten" generator-info-url="http://www.webgrabplus.com">')
for href in hrefs:
# print href.attrib['href']
 canal = href.attrib['href'].split('/')[4]
 print canal
 for numdias in range(0, 6):
  d2 = today + timedelta(days=numdias)
  print d2.strftime("%Y%m%d")
  diasemana = weekDays[d2.weekday()]
  page = requests.get(href.attrib['href']+diasemana)
  print href.attrib['href'] + diasemana
  tree = html.fromstring(page.content)
  timex = tree.xpath('.//p[@class="article-info ml10 fs14 left"]/.//b/text()')
  resumo = tree.xpath('.//b[@class="ml10 black_gray"]/text()')
  descricao = tree.xpath('.//p[contains(@class,"p10 channel_desc")]/text()')
  for i in range(len(timex)):
    timestamp = timex[i].split()
    start_date = str(d2.strftime("%Y%m%d"))+str(timestamp[0].replace(":","")+str("00 +0000"))
    end_date = str(d2.strftime("%Y%m%d"))+str(timestamp[2].replace(":","")+str("00 +0000"))
#   print 'resumo:', resumo[i]
    desc = ''
    if len(descricao):
      desc = descricao[i]
      desc = desc.replace( '&', '&amp;')
      desc = desc.replace( '<', '&lt;')
      desc = desc.replace( '>', '&gt;')
      desc = desc.replace('\\', '&quot;')

    resumo[i] = resumo[i].replace( '&', '&amp;')
    resumo[i] = resumo[i].replace( '<', '&lt;')
    resumo[i] = resumo[i].replace( '>', '&gt;')
    resumo[i] = resumo[i].replace('\\', '&quot;')

    ligne1 = '<programme start="'+ str(start_date) + '" stop="' + str(end_date) + '" channel="'+canal+'">'
    ligne2 = '  <title lang="pt">' + resumo[i] + ' </title>'
    ligne3 = '  <desc lang="pt">' + desc +'</desc>'
    ligne4 = '</programme>'
  

#  <programme start="20200117070000 +0000" stop="20200117075500 +0000" channel="PT-ID_INVESTIGATION_DISCOVERY">
#    <title lang="pt">Shadow Of Doubt T.1 Ep.3</title>
#    <category lang="pt">documentarios</category>
#    <episode-num system="xmltv_ns">T.1 Ep.3</episode-num>
#  </programme>
#    print ligne1.encode('utf-8').strip()
#    print ligne2.encode('utf-8').strip()
#    print ligne3.encode('utf-8').strip()
    
    file.write(ligne1.encode('utf-8').strip()+'\n')
    file.write(ligne2.encode('utf-8').strip()+'\n')
    file.write(ligne3.encode('utf-8').strip()+'\n')
    file.write(ligne4.encode('utf-8').strip()+'\n')
file.write('</tv>')    
file.close()    
