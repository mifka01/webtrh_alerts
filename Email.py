import settings
import json
import requests
from bs4 import BeautifulSoup


class Email:

    def __init__(self):
        self.login_data = {
            'vb_login_username': settings.USERNAME,
            'vb_login_password': settings.PASSWORD,
            's': None,
            'securitytoken': 'guest',
            'do': 'login',
            'vb_login_md5password': None,
            'vb_login_md5password_utf': None
            }

    def get_mails_to_send(self):
        response = requests.get('https://api.pushbullet.com/v2/pushes',
                            headers={'Authorization': 'Bearer ' + settings.ACCESS_TOKEN, 'Content-Type': 'application/json'})
        pushes = [push for push in json.loads(response.text)["pushes"][:10] if "body" in push.keys() and push["active"]]
        codes = {push["body"][-4:]: push["iden"] for push in pushes if "/mail" in push["body"][-10:]}
        mails = [{"recipient": push["body"].splitlines()[1],
                  "title":push["body"].splitlines()[0],
                  "iden":push["iden"],
                  "command_iden": codes[push["body"][-4:]]} for push in pushes if push["body"][-4:] in codes.keys() and len(push["body"]) > 10]
        return mails

    def send_mail(self, recipient, title, message):
        email_data = {
        "recipients": recipient,
        'bccrecipients': None,
        'title': f'Re: {title}',
        'message': message,
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
        with requests.Session() as session:
            session.post("https://webtrh.cz/login.php?do=login", data=self.login_data)
            source = session.get('https://webtrh.cz/private.php?do=newpm')
            soup = BeautifulSoup(source.content, 'lxml')
            email_data["securitytoken"] = soup.find("input", {"name": "securitytoken"})["value"]
            resp = session.post('https://webtrh.cz/private.php?do=insertpm&pmid=', data=email_data)
        session.close()
