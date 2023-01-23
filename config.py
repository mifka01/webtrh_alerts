from os import environ as env
from dotenv import load_dotenv

load_dotenv()

# Discord token
DISCORD_TOKEN = env['DISCORD_TOKEN']

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

# CSS Selectors
DEAL_ROW_SELECTOR = "tr.threadbitX"
TITLE_SELECTOR = "a.title"
AUTHOR_SELECTOR = "a.username"
POSTBODY_SELECTOR = "div.postbody"
BUDGET_SELECTOR = "span#vbpas_cena_poptavky1"

# Guild join message
GUILD_JOIN_MESSAGE = """
I'm now in your server!\nPlease set me a main channel in your server with `/set channel` command
"""
