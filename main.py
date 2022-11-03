import requests
from bs4 import BeautifulSoup
import re
import json

url = "https://rasp.rea.ru/Schedule/ScheduleCard"

querystring = {"selection":"15.25д-экф05/20б","weekNum":'1',"catfilter":"0"}

payload = ""
headers = {
    "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    "Accept": "text/html, */*; q=0.01",
    "Referer": "https://rasp.rea.ru/?q=15.25%D0%B4-%D1%8D%D0%BA%D1%8405%2F20%D0%B1",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": '"Windows"'
}

response_dict = {}
for n in range(1, 21):
    querystring["weekNum"] = str(n)
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring).text
    page = re.sub('<br/>', ' ', response)

    soup = BeautifulSoup(page, 'html.parser')
    week_dict = {}
    for day in soup.find_all('div', {'class': 'container'}):
        d = day.find('th', {'class': 'dayh'}).text
        day_dict = dict()
        for slot in day.find_all('tr', {'class':'slot'}):
            time = slot.find('td').text.strip()
            if slot.find('span', {'class': 'pcap'}):
                time = time[:6] + ' ' + time[6:11] + '-' + time[11:]
            if slot.find('a', {'class': 'task'}):
                c = ' '.join(re.sub('\r\n', '', slot.find('a', {'class': 'task'}).text).split())
            else:
                c = []
            day_dict[time] = c
        week_dict[d] = day_dict
    response_dict[f'{n} НЕДЕЛЯ'] = week_dict
with open('parsed.json', encoding='utf-8', mode='w') as parsed:
    json.dump(response_dict, parsed, indent=4, ensure_ascii=False)
