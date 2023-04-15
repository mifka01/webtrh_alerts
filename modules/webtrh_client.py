from os import wait
from sys import exit

import requests
from bs4 import BeautifulSoup as bs

from config import DEAL_ROW_SELECTOR, OLD_WEBTRH_STYLE_LINK, WEBTRH_LINK
from modules.database import DBClient
from modules.deal import Deal


class WBClient():
    def __init__(self):
        self.database = DBClient()
        self.session = requests.Session()
        # Load old webtrh website design
        try:
            self.session.get(OLD_WEBTRH_STYLE_LINK)
        except Exception:
            print(f'[error] {OLD_WEBTRH_STYLE_LINK} is not accessible')
            print('[info] turning off...')
            exit(1)

        self.set_categories()
        self.current_deals_ids = set()
        self.saved_deals_ids = set()
        self.get_deals()

    def set_categories(self):
        sql = 'SELECT id, code FROM category'
        self.categories = self.database.query(sql, fetchall=True)

    def get_guild_categories(self, guild_id):
        sql = 'SELECT category_id FROM guild_categories WHERE guild_id = %s'
        cats = self.database.query(sql, [guild_id], fetchall=True)
        return [cat['category_id'] for cat in cats]

    def read_saved_deals(self, category):
        sql = "SELECT deal.id FROM deal where category = %s"

        deals = self.database.query(sql, [category['id']], fetchall=True)

        self.saved_deals_ids = set([deal['id'] for deal in deals])

    def write_deals(self, new_deals):
        sql = "INSERT INTO deal (id, category) VALUES (%s, %s)"
        values = [(deal.id, deal.category['id']) for deal in new_deals]

        self.database.query(sql, values, many=True, commit=True)
        new_deals_len = len(new_deals)
        if (new_deals_len):
            print(f"[info] inserted: {new_deals_len} new rows")

    def remove_old_deals(self):
        remove = self.saved_deals_ids.difference(self.current_deals_ids)
        remove_len = len(remove)
        if (remove_len > 0):
            sql = "DELETE FROM deal WHERE id IN (%s)" % ",".join([
                "%s"] * remove_len)
            self.database.query(sql, list(remove), commit=True)
            self.current_deals_ids = set()
            print(f"[info] removed {remove_len} old deals")

    def get_deals(self):
        new_deals = set()
        for category in self.categories:
            self.read_saved_deals(category)

            try:
                source = self.session.get(WEBTRH_LINK + category['code'])
            except Exception:
                print(
                    f'[error] {WEBTRH_LINK + category["code"]} is not accessible')
                continue

            soup = bs(source.content, 'lxml')

            for deal_soup in soup.select(DEAL_ROW_SELECTOR):
                try:
                    deal = Deal(deal_soup, category, self.session)
                except Exception:
                    print('[error] cant create Deal object')
                    continue

                self.current_deals_ids.add(deal.id)

                if (deal.id not in self.saved_deals_ids):
                    new_deals.add(deal)

        self.write_deals(new_deals)
        return new_deals
