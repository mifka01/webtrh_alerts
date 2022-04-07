from config import (
        SEND_EMAIL_PREFIX,
        LOGIN_DATA,
        PUSHBULLET_PUSH_URL,
        PUSHBULLET_HEADERS,
        EMAIL_DATA,
        SEND_MAIL_REQUEST_URL,
        LOGIN_REQUEST_URL,
        NEW_MAIL_URL
        )
import json
import requests
from bs4 import BeautifulSoup


class Email:

    def __init__(self):
        self.login_data = LOGIN_DATA

    def get_mails_to_send(self):
        response = requests.get(
                PUSHBULLET_PUSH_URL,
                headers=PUSHBULLET_HEADERS
                )

        pushes = []
        for push in json.loads(response.text)['pushes'][:-10]:
            if push.get('active') and push.get('body') is not None:
                pushes.append(push)

        mails = []
        codes = self.get_send_codes(pushes)
        for push in pushes:
            body = push.get('body')
            code = body[-4:]
            if code in codes and len(body) > 10:
                mails.append({
                    'recipient': body.splitlines()[2],
                    'title': push.get('title'),
                    'iden': push.get('title'),
                    'command_iden': codes.get(code)
                    })
        return mails

    def get_send_codes(self, pushes):
        codes = {}
        for push in pushes:
            body = push.get('body')
            if SEND_EMAIL_PREFIX in body[-10:]:
                code = body[-4:]
                codes[code] = push['iden']
        return codes

    def send_mail(self, recipient, title):
        email_data = EMAIL_DATA
        email_data['recipients'] = recipient
        email_data['title'] = f'Re: {title}'

        with requests.Session() as session:
            session.post(LOGIN_REQUEST_URL, data=LOGIN_DATA)
            source = session.get(NEW_MAIL_URL)
            soup = BeautifulSoup(source.content, 'lxml')
            token = soup.select_one('input[name="securitytoken"]').get('value')
            email_data["securitytoken"] = token
            session.post(SEND_MAIL_REQUEST_URL, data=email_data)
        session.close()
