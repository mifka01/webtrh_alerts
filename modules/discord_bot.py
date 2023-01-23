from discord.ext import tasks, commands
from discord import Object
from modules.webtrh_client import WBClient
from modules.message import Message
from config import TASK_LOOP, GUILD_JOIN_MESSAGE
from datetime import datetime


class DCBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, command_prefix='!')
        self.webtrh = WBClient()

    async def get_channel(self, guild_id):
        guild = self.get_guild(guild_id)
        sql = "SELECT channel_id from guild where id = %s"
        channel_id = self.webtrh.database.query(sql, [guild.id], fetchone=True)['channel_id']
        if(channel_id is None):
            try:
                await guild.owner.send(GUILD_JOIN_MESSAGE)
            except Exception:
                print(f"{guild.owner} has their dms turned off")
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        await channel.send(GUILD_JOIN_MESSAGE)
                        break
            return None
        return await self.fetch_channel(channel_id)

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.send_new_jobs.start()

    async def on_ready(self):
        print(f'[info] Logged in as {self.user} (ID: {self.user.id})')
        print('--------------------')

    @tasks.loop(seconds=TASK_LOOP)
    async def send_new_jobs(self):
        print(f'[loop] {datetime.now():%d.%m.%Y %H:%M:%S}')
        new_deals = self.webtrh.get_deals()
        async for guild in self.fetch_guilds(limit=150):
            channel = await self.get_channel(guild.id)
            if(channel is None):
                continue

            for deal in new_deals:
                message = Message(deal)
                await channel.send(embed=message)
                print(f"[info] deal {deal.id} has been sent to {guild.name}")
        self.webtrh.remove_old_deals()

    async def on_guild_join(self, guild):
        sql = "INSERT INTO guild (id, channel_id) VALUES (%s, %s)"
        values = (guild.id, None)
        self.webtrh.database.query(sql, values, commit=True)

        try:
            await guild.owner.send(GUILD_JOIN_MESSAGE)
        except Exception:
            print(f"{guild.owner} has their dms turned off")
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    await channel.send(GUILD_JOIN_MESSAGE)
                    break

    @send_new_jobs.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in
