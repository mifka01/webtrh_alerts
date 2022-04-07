from pathlib import Path
from os import environ as env
from dotenv import load_dotenv

load_dotenv()

# List of categories to alert from
WEBTRH_CATEGORIES = ['https://webtrh.cz/f101']

# Edit EMAIL MESSAGE in <message.txt> file
EMAIL_MESSAGE = Path('message.txt').read_text()
if 'EMAIL_MESSAGE' in env and env['EMAIL_MESSAGE'] != "":
    EMAIL_MESSAGE = env['EMAIL_MESSAGE']

# Send email command prefix
SEND_EMAIL_PREFIX = '/mail'

# Webtrh login request url
LOGIN_REQUEST_URL = 'https://webtrh.cz/login.php?do=login'

# Webtrh new mail url
NEW_MAIL_URL = 'https://webtrh.cz/private.php?do=newpm'

# Webtrh send mail request url
SEND_MAIL_REQUEST_URL = 'https://webtrh.cz/private.php?'

# Pushbullet api key
PUSHBULLET_API_KEY = env['PUSHBULLET_API_KEY']

# Pushbullet push url
PUSHBULLET_PUSH_URL = env['PUSHBULLET_PUSH_URL']

# Pushbullet headers
PUSHBULLET_HEADERS = {
                    'Authorization': f"Bearer {PUSHBULLET_API_KEY}",
                    'Content-Type': 'application/json'
                    }
# Webtrh login request data
LOGIN_DATA = {
            'vb_login_username': env['WEBTRH_USERNAME'],
            'vb_login_password': env['WEBTRH_PASSWORD'],
            's': None,
            'securitytoken': 'guest',
            'do': 'login',
            'vb_login_md5password': None,
            'vb_login_md5password_utf': None
            }

# Email request data
EMAIL_DATA = {
                "recipients": '',
                'bccrecipients': None,
                'title': '',
                'message': EMAIL_MESSAGE,
                'sbutton': 'Odeslat příspěvek',
                's': None,
                'securitytoken': None,
                'receipt': 0,
                'savecopy': 1,
                'signature': 0,
                'parseurl': 1,
                'disablesmilies': 1,
                'do': 'insertpm',
                'pmid': None,
                'forward': None,
            }
