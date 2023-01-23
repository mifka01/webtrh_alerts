from discord import Intents
from valid_dotenv import valid_environment
from sys import exit
from modules.discord_bot import DCBot
from config import DISCORD_TOKEN
from commands import setup
import asyncio


async def main():
    print('[info] Starting WB Alerts')
    print('[info] Checking Enviroment settings ')
    if (valid_environment()):
        print('[info] Running...')
        print('--------------------')

        intents = Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True

        bot = DCBot(intents=intents)
        async with bot:
            await setup(bot)
            await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
