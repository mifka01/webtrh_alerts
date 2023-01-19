from os import wait
import requests
from bs4 import BeautifulSoup as bs
from modules.database import DBClient
from config import WEBTRH_LINK, OLD_WEBTRH_STYLE_LINK, DEAL_ROW_SELECTOR
from modules.deal import Deal


class WBClient():
    def __init__(self):
        self.database = DBClient()
        self.session = requests.Session()
        # Load old webtrh website design
        self.session.get(OLD_WEBTRH_STYLE_LINK)

        self.set_categories()
        self.current_deals_ids = set()
        self.saved_deals_ids = set()
        self.get_deals()

    def set_categories(self):
        sql = 'SELECT id, code FROM category'
        self.categories = self.database.query(sql, fetchall=True)

    def read_saved_deals(self, category):
        sql = "SELECT deal.id FROM deal where category = %s"

        deals = self.database.query(sql, [category['id']], fetchall=True)

        self.saved_deals_ids = set([deal['id'] for deal in deals])

    def write_deals(self, new_deals):
        sql = "INSERT INTO deal (id, category) VALUES (%s, %s)"
        values = [(deal.id, deal.category['id']) for deal in new_deals]

        self.database.query(sql, values, many=True)
        self.database.commit()

        print(f"[info] inserted: {len(new_deals)} new rows")

    def remove_old_deals(self):
        remove = self.saved_deals_ids.difference(self.current_deals_ids)

        sql = "DELETE FROM deal WHERE id = %s"
        for deal_id in remove:
            self.database.query(sql, [deal_id])
        self.current_deals_ids = set()

    def get_deals(self):
        new_deals = set()
        for category in self.categories:
            self.read_saved_deals(category)

            try:
                source = self.session.get(WEBTRH_LINK + category['code'])
            except Exception as e:
                print(e)
                continue

            soup = bs(source.content, 'lxml')

            for deal_soup in soup.select(DEAL_ROW_SELECTOR):
                try:
                    deal = Deal(deal_soup, category, self.session)
                except Exception as e:
                    print(e)
                    continue

                self.current_deals_ids.add(deal.id)

                if(deal.id not in self.saved_deals_ids):
                    new_deals.add(deal)

        self.write_deals(new_deals)
        return new_deals
