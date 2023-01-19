from discord import Intents
from valid_dotenv import valid_environment
from sys import exit
from modules.discord_client import DClient
from config import DISCORD_TOKEN


if __name__ == "__main__":
    print('[info] Starting WT Alerts')
    print('[info] Checking Enviroment settings ')
    if (valid_environment()):
        print('[info] Running...')
        print('--------------------')
        client = DClient(intents=Intents.default())
        client.run(DISCORD_TOKEN)
    exit(1)
