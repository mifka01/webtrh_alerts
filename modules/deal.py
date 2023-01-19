from config import (
    THREAD_ID_PREFIX_LEN,
    WEBTRH_LINK,
    TITLE_SELECTOR,
    AUTHOR_SELECTOR,
    BUDGET_SELECTOR,
    POSTBODY_SELECTOR
)
from bs4 import BeautifulSoup as bs


class Deal(object):
    def __init__(self, deal, category, session):
        self.soap = deal
        self.id = None
        self.category = category
        self.session = session
        self.title = None
        self.link = WEBTRH_LINK + str(self.id)
        self.author = None
        self.post_body = None
        self.detail_soup = None
        self.budget = None

    @property
    def id(self):
        if(self._id is None):
            self._id = int(self.soap.get('id')[THREAD_ID_PREFIX_LEN:])
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def title(self):
        if(self._title is None):
            self._title = self.soap.select_one(TITLE_SELECTOR).text.strip()
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def detail_soup(self):
        if(self._detail_soup is None):
            source = self.session.get(self.link)
            self._detail_soup = bs(source.content, 'lxml')
        return self._detail_soup

    @detail_soup.setter
    def detail_soup(self, value):
        self._detail_soup = value

    @property
    def author(self):
        if(self._author is None):
            self._author = self.detail_soup.select_one(AUTHOR_SELECTOR).text.strip()
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def post_body(self):
        if(self._post_body is None):
            self._post_body = self.detail_soup.select_one(POSTBODY_SELECTOR).text.strip()
        return self._post_body

    @post_body.setter
    def post_body(self, value):
        self._post_body = value

    @property
    def budget(self):
        if(self._budget is None):
            self._budget = self.detail_soup.select_one(BUDGET_SELECTOR).text.strip()
        return self._budget

    @budget.setter
    def budget(self, value):
        self._budget = value
