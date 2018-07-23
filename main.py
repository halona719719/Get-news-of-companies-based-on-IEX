from bs4 import BeautifulSoup
import re
import requests
import json


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def get_symbols():
   r = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
   json_file = json.loads(r.text)
   symbols = [j['symbol'].lower() for j in json_file]
   return symbols

company_list = []
company_list = get_symbols()

json_data = []

def read_news_url(r_url):
    resp = r_url
    soup = BeautifulSoup(resp.text, "lxml")
    divs = soup.findAll("div", {"itemprop": "articleBody"})
    divs = cleanhtml(str(divs))
    return divs


i = 1
for company in company_list:
    link = "https://api.iextrading.com/1.0/stock/" + company + "/news"
    r = requests.get(link)
    json_file = json.loads(r.text)
    for j in json_file:
        news_url = j['url']
        r_url = requests.get(news_url)
        if r_url.status_code == 200:
            news_content = read_news_url(r_url)
        else:
            news_content = ''
        j['content'] = news_content
    json_data_temp = {company: json_file}
    json_data.append(json_data_temp)
with open('../datasets/news/company_news.json', 'w') as outf:
    json.dump(json_data, outf)
