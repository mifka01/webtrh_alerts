import requests
import os
import json
import csv
from bs4 import BeautifulSoup
import time
from settings import ACCESS_TOKEN, MESSAGE
import random
import string
from Email import Email


class Alert(Email):

    def __init__(self):
        super().__init__()

    def get_deals(self):
        deals = []
        source = requests.get('https://webtrh.cz/f101')
        soup = BeautifulSoup(source.content, 'lxml')
        deals_scraped = [deal.find("div", class_="deal-column title")
                         for deal in soup.find_all("div", class_="deal-row")]
        for deal in deals_scraped[1:]:
            link = self.clean(deal.find("a")["href"])
            title = self.clean(deal.text)
            deals.append({"title": title,
                          "link": link})
        return deals

    def get_deal_details(self, link):
        source = requests.get(link)
        soup = BeautifulSoup(source.content, 'lxml')
        article = self.clean(
            soup.find('blockquote', class_='postcontent').text)
        budget = self.clean(soup.find(
            'span', class_='vbpas_cena_poptavky1').text)
        numbers = soup.find('table', {'class': 'vbpas_deal_info'})
        numbers = self.clean(numbers.find_all(
            'tr')[2].text)
        seller = self.clean(soup.find('a', {'class': 'username'}).text)
        return {"article": article, "budget": budget, "numbers": numbers, "seller": seller}

    def run(self):
        old_deals = self.get_deals()
        while True:
            new_deals = [deal for deal in self.get_deals()
                         if deal not in old_deals]
            if len(new_deals) > 0:
                for deal in new_deals:
                    data = self.get_deal_details(deal["link"])
                    data["title"] = deal["title"]
                    data["link"] = deal["link"]
                    self.send_notification(data)
                    old_deals.append(deal)
            mails = self.get_mails_to_send()
            if len(mails) > 0:
                for mail in mails:
                    self.send_mail(mail["recipient"], mail["title"], MESSAGE)
                    self.delete_notification(mail["iden"])
                    self.delete_notification(mail["command_iden"])
            time.sleep(60)

    def clean(self, bloated_string) -> str:
        if "\n" in bloated_string:
            if bloated_string.startswith("\n"):
                bloated_string.replace("\n", "")
            bloated_string.replace("\n", "<br>")
        return " ".join(bloated_string.strip().split())

    def send_notification(self, data):
        data = {"type": "note", "title": 'Nová pracovní nabídka',
                "body": f"{data['title']}\n{data['seller']}\n\n{data['article']}\n\n{data['link']}\n{self.get_code()}"}
        resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data),
                             headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
        if resp.status_code != 200:
            raise Exception('Something wrong')
        else:
            print('New deal sent!')

    def get_code(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(4))

    def delete_notification(self, iden):
        requests.delete(
            url=f"https://api.pushbullet.com/v2/pushes/{iden}", headers={'Access-Token': ACCESS_TOKEN})
