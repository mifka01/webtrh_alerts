import engine
import alert

old_titles, old_links = engine.get_deals()


while True:
    new_deals = []
    new_titles, new_links = engine.get_deals()
    for i in range(len(new_titles)):
        if new_titles[i] not in old_titles and new_links[i] not in old_links:
            new_deals.append({"title":new_titles[i],"link":new_links[i]})

    if len(new_deals) > 0:
        for deal in new_deals:
            article, _, _ = engine.get_deal_details(deal['link'])
            alert.send_notification_via_pushbullet('Nová pracovní nabídka', f"{deal['title']}\n{article}\n{deal['link']}")
            old_titles.append(deal['title'])
            old_links.append(deal['link'])
