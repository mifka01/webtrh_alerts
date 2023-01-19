from os import environ as env
from dotenv import load_dotenv


def valid_environment() -> bool:
    load_dotenv()

    required = ["DISCORD_TOKEN",
                "DISCORD_CHANNEL_ID",
                "MYSQL_HOST",
                "MYSQL_USER",
                "MYSQL_DATABASE",
                "MYSQL_PASSWORD"]

    for var in required:
        try:
            env[var]
        except KeyError:
            print(f'[error] `{var}` enviroment variable required')
            return False

        if (env[var] == ""):
            print(f'[error] `{var}` enviroment variable cannot be empty')
            return False

    print('[info] Enviroment successfully loaded')
    return True
