from os import environ as env
from dotenv import load_dotenv

load_dotenv()

# Discord token
DISCORD_TOKEN = env['DISCORD_TOKEN']

# Discord channel
DISCORD_CHANNEL_ID = int(env['DISCORD_CHANNEL_ID'])

# https://gist.github.com/thomasbnt/b6f455e2c7d743b796917fa3c205f812
MESSAGE_COLOR = 7419530

# Scraping task loop in seconds
TASK_LOOP = 60

# MYSQL database credentials
MYSQL_HOST = env['MYSQL_HOST']
MYSQL_USER = env['MYSQL_USER']
MYSQL_DATABASE = env['MYSQL_DATABASE']
MYSQL_PASSWORD = env['MYSQL_PASSWORD']

# Webtrh
WEBTRH_LINK = "https://webtrh.cz/"
OLD_WEBTRH_STYLE_LINK = "https://webtrh.cz/index.php?styleid=5"
THREAD_ID_PREFIX_LEN = 7
DEAL_ROW_SELECTOR = "tr.threadbitX"
