import engine
import alert
from symbol import get_symbol
from email_manager import get_emails_to_send, send_email
from sended import delete_message
import time
import os

old_titles, old_links = engine.get_deals()
print('Webtrh Alerts active')
print('Running..')
print('--------------------')

while True:
    new_deals = []
    new_titles, new_links = engine.get_deals()
    for i in range(len(new_titles)):
        if new_titles[i] not in old_titles and new_links[i] not in old_links:
            new_deals.append({"title":new_titles[i],"link":new_links[i]})

    if len(new_deals) > 0:
        for deal in new_deals:
            article, _, _, seller = engine.get_deal_details(deal['link'])
            alert.send_notification_via_pushbullet('Nová pracovní nabídka', f"{deal['title']}\n{seller}\n{article}\n{deal['link']}\n{get_symbol()}")
            old_titles.append(deal['title'])
            old_links.append(deal['link'])

    emails = get_emails_to_send()
    if len(emails) == 0:
        pass
    else:
        for email in emails:
            print(f"email poslán {email['recipient']} {email['title']}")
            send_email(email['recipient'],email['title'],str(os.environ.get('message_text')))
            delete_message(email['iden'])  
            delete_message(email['resp_iden'])  
    time.sleep(60)
