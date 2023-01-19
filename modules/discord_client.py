from discord.ext import tasks
import discord
from modules.webtrh_client import WBClient
from modules.message import Message
from config import DISCORD_CHANNEL_ID, TASK_LOOP


class DClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.webtrh = WBClient()

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.send_new_jobs.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=TASK_LOOP)
    async def send_new_jobs(self):
        for deal in self.webtrh.get_deals():
            message = Message(deal)
            await self.channel.send(embed=message)
        self.webtrh.remove_old_deals()

    @send_new_jobs.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in
        self.channel = self.get_channel(DISCORD_CHANNEL_ID)



