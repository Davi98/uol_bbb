from cgi import test
from lib2to3.pgen2.token import PERCENT
import os
from time import timezone
from dotenv import load_dotenv
import json
from requests_html import HTML, HTMLSession
from Brother import Brother
import re
import tweepy as tw
from datetime import datetime
from datetime import timedelta
load_dotenv()
url = os.environ.get("URL")


consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


session = HTMLSession()
response_page = session.get(url)
ids_elem = response_page.html.find('.checkbox')
names_elem = response_page.html.find('.answer-title')
vote_id_elem = response_page.html.xpath(
    '/html/body/article/div[2]/div/div[1]/div/div[2]/div[1]/div[4]/div[1]')
# vote_id = (re.sub(
#     ";.*", "", vote_id_elem[0].attrs['ng-init']).replace("id=", "")).strip('\"')
vote_id = 58490
result_url = f"https://enquete.uol.com.br/results?format=jsonp&jsonp=angular.callbacks._0&id={vote_id}&"
result_headers = {
    'authority': 'enquete.uol.com.br',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'sec-ch-ua-platform': '"Linux"',
    'accept': '*/*',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-dest': 'script',
    'referer': 'https://www.uol.com.br/splash/bbb/enquetes/2022/01/24/quem-deve-ser-eliminado-do-bbb-22.htm',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': '_ga=GA1.3.1830952918.1640025569; __tbc=%7Bkpbx%7DYgkb44Vde9iu-zRH3lHVIjyliGfyEaejaCoWZlE5YKs; cX_P=kxf0vonahut00xjr; BTCTL=ad; _fbp=fb.2.1640025570651.1433274017; cX_G=cx%3A2znxv9rwori0c3w4zk54lo7ktw%3Aamx6s34emtcq; _hjSessionUser_1864078=eyJpZCI6ImMwOWQ5ZjgxLTFmNzktNTRiMi05ZDEwLTNlZGMwNjY0Mjc5NSIsImNyZWF0ZWQiOjE2NDAwMjU1Njk0NzAsImV4aXN0aW5nIjp0cnVlfQ==; __gads=ID=36bd6bd19671ff16:T=1640025571:S=ALNI_MZu8uIYOGCBk7nVcdphd9oSb9j7Qg; _ugfc=1; _gid=GA1.3.1609434765.1643054182; __pat=10800000; xbc=%7Bkpbx%7DpodW-Y9ICV-UIErocFV6liDq_wdVgw0iYtNxAICO4LatUOJDbqBlTPpdD8uqyYoeeMIP5mDR7W9R0Sfp5ouhnCXIx6SfWjPl5uqkNJGETEJpvCRpI_qxQQfmcQf2C6M3na3Aj8xwIPg5HKe2HkFrfr1CGliXB1G1OlJRI6saM45yzdICzK_aAAzhn-ZUlsyf; _hjSessionUser_1969075=eyJpZCI6IjMwOTM4NjRkLWM0NjctNWM0ZC04NzU2LWVkNWQ1ZWM4M2UzYyIsImNyZWF0ZWQiOjE2NDMwNTQxODIyOTQsImV4aXN0aW5nIjp0cnVlfQ==; cX_S=kyt6860dphjvzlkq; _hjSession_1969075=eyJpZCI6IjE0ZWZlMzAxLWVlYTktNDMyNC1iZDIzLTA2Mjc2OTNkNmNiNyIsImNyZWF0ZWQiOjE2NDMwNzE0ODI3MjQsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; __pvi=%7B%22id%22%3A%22v-kytec6m5qc68glx1%22%2C%22domain%22%3A%22.uol.com.br%22%2C%22time%22%3A1643071875081%7D; FCNEC=[["AKsRol9qZs5IqgyHPyPcEIpWEVLHlJY_DK4SB9oXxAfi53sbb2RWTZexLS2yzjBaegFcp-bPRW7hTFHdO_m0Dnv9T_Rnieowl0ov8BNG-uVEf2aSieCcx9htYLSV3FNuzair1PDIazvQRzgpOuEUaJOD9R4lyScuYQ=="],null,[]]; _gat_uolMain=1'
}
response_results = session.get(result_url, headers=result_headers)
brothers = []

json_result_response = json.loads(response_results.text.replace(
    "angular.callbacks._0(", "").replace(")", ""))
answers = json_result_response['answers']

for i in range(0, len(ids_elem)):
    name = names_elem[i].text
    id = (ids_elem[i].attrs['for']).replace("radio-", "")
    for y in range(0, len(answers)):
        if (id) == str(answers[y]['id']):
            percentage = answers[y]['percent']
            votes = answers[y]['votes']

    brothers.append(
        Brother(name=name, id=id, percentage=percentage, num_votes=votes))


brothers_order = sorted(brothers, key=lambda x: x.num_votes, reverse=True)

date = datetime.now() - timedelta(hours=3)

if date.day < 10:
   day = "0" + str(date.day)
else:
    day = date.day

if date.hour < 10:
   hour = "0" + str(date.hour)
else:
    hour = date.hour

if date.minute < 10:
   minute = "0" + str(date.minute)
else:
    minute = date.minute

total_votes = format(json_result_response['votes'],',d').replace(",",".")
total_votes_0 =  format(brothers_order[0].num_votes,',d').replace(",",".")
total_votes_1 = format(brothers_order[1].num_votes,',d').replace(",",".")
total_votes_2 = format(brothers_order[2].num_votes,',d').replace(",",".")



status = f"Total de votos: {total_votes} no dia {day}/0{date.month} as {hour}:{minute} \n\n1° {brothers_order[0].name} com {brothers_order[0].percentage}% da votação totalizando {total_votes_0} votos\n\n2° {brothers_order[1].name} com {brothers_order[1].percentage}% da votação totalizando {total_votes_1} votos\n\n3° {brothers_order[2].name} com {brothers_order[2].percentage}% da votação totalizando {total_votes_2} votos \n"


api.update_status(status=status)
