import requests
import json
from bs4 import BeautifulSoup
import time
import random
import string
from Email import Email
from config import (
        WEBTRH_CATEGORIES,
        PUSHBULLET_PUSH_URL,
        PUSHBULLET_HEADERS,
        PUSHBULLET_API_KEY
        )


class Alert(Email):

    def __init__(self):
        super().__init__()

    def get_deals(self):
        deals = []
        for category in WEBTRH_CATEGORIES:
            source = requests.get(category)
            soup = BeautifulSoup(source.content, 'lxml')

            for deal in soup('div', class_='deal-column title', limit=36)[1:]:
                deals.append(deal.find('a')['href'])

        return deals

    def soup_lookup(self, link, selectors):
        source = requests.get(link)
        soup = BeautifulSoup(source.content, 'lxml')
        data = {}

        for key, selector in selectors.items():
            if (type(selector) is list):
                data[key] = soup.select(selector[0])[selector[1]].text
            else:
                data[key] = soup.select_one(selectors[key]).text
            data[key] = self.clean(data[key])
        return data

    def get_deal_details(self, link):
        return self.soup_lookup(link, {
                'title': 'h1',
                'article': 'div.article',
                'budget': ['div.meta-box div.value', 2],
                'seller': 'div.people div.dropdown-text',
                'numbers': ['div.info-box div.down', 1]
            })

    def run(self):
        old_deals = self.get_deals()
        while True:
            new_deals = [x for x in self.get_deals() if x not in old_deals]
            if (len(new_deals)):
                for deal in new_deals:
                    data = self.get_deal_details(deal)
                    data["link"] = deal
                    self.send_notification(data)
                    old_deals.insert(0, deal)
                    old_deals.pop()
            mails = self.get_mails_to_send()
            if len(mails):
                for mail in mails:
                    self.send_mail(mail["recipient"], mail["title"])
                self.delete_notification(mail["iden"])
                self.delete_notification(mail["command_iden"])
            time.sleep(60)

    def clean(self, bloated_string: str) -> str:
        if "\n" in bloated_string:
            if bloated_string.startswith("\n"):
                bloated_string.replace("\n", "")
            bloated_string.replace("\n", "<br>")
        return " ".join(bloated_string.strip().split())

    def send_notification(self, data):
        notification_text = {
            "type": "note",
            "title": data['title'],
            "body":
            f"""{data['budget']}\n{data['numbers']}\n{data['seller']}
            \n{data['article']}
            \n{data['link']}\n{self.get_code()}"""}

        response = requests.post(
                PUSHBULLET_PUSH_URL,
                data=json.dumps(notification_text),
                headers=PUSHBULLET_HEADERS
                )

        if response.status_code != 200:
            raise Exception(f"[error] Cant reach {PUSHBULLET_PUSH_URL}")
        print('[info] Notification sent')

    def get_code(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(4))

    def delete_notification(self, iden):
        response = requests.delete(
                url=f"{PUSHBULLET_PUSH_URL}/{iden}",
                headers={'Access-Token': PUSHBULLET_API_KEY}
                )
        if response.status_code != 200:
            raise Exception(f"[error] Cant reach {PUSHBULLET_PUSH_URL}/{iden}")
