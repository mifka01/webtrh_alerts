from discord import Embed
from config import MESSAGE_COLOR
from datetime import datetime


class Message(Embed):
    def __init__(self, deal) -> None:
        super().__init__()
        self.deal = deal
        self.title = deal.title
        self.url = deal.link
        self.description = self.compose_description()
        self.color = MESSAGE_COLOR
        self.timestamp = datetime.now()

    def compose_description(self):
        return f"""
        {self.deal.author}
        {self.deal.budget}

        {self.deal.post_body}
        """
