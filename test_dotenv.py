from os import environ as env
from dotenv import load_dotenv


def valid_environment() -> bool:
    load_dotenv()

    required = ["PUSHBULLET_API_KEY",
                "PUSHBULLET_PUSH_URL",
                "WEBTRH_USERNAME",
                "WEBTRH_PASSWORD",
                ]

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
