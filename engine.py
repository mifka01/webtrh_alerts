from bs4 import BeautifulSoup
import requests
import csv


def get_deals():
    new_titles = []
    new_links = []
    result = requests.get('https://webtrh.cz/f101')
    source = result.content
    soup = BeautifulSoup(source, 'lxml')
    deals = soup.find_all("div",{"class":"deal-row"})        
    for deal in deals[1:]:
        deal = deal.find("div", {"class":"deal-column title"})
        new_titles.append(deal.text.strip())
        new_links.append(deal.find("a")["href"].strip())
    return new_titles, new_links
        

def write_deals():
    titles, links = get_deals()
    with open('webtrh/deals.csv', 'w', newline='') as file:
        fieldnames = ['title','link']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({'title': "title", 'link': "link"})
        for title, link in zip(titles, links):
            writer.writerow({'title': title, 'link': link})
    print("Databáze byla aktualizována")
    file.close()


def read_deals():
    old_titles = []
    old_links = []
    with open('deals.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            old_titles.append(row["title"])
            old_links.append(row["link"])
    csvfile.close()
    return old_titles, old_links


def get_deal_details(link):
    result = requests.get(link)
    source = result.content
    soup = BeautifulSoup(source, 'lxml')
    article = soup.find('div', {'class': 'padding-30 article'}).text.strip()
    budget = soup.find_all('div', {'class':'col-xs-6 padding-10-0'})[2].text
    budget = " ".join(budget.split())
    numbers = soup.find('div', {'class': 'row padding-20-0'})
    numbers = numbers.find_all('div',{'class':'col-xs-6'})[1].text
    numbers = " ".join(numbers.split())

    

    return article, budget, numbers


def get_new_deals():
    new_deals = []
    new_titles, new_links = get_deals()
    old_titles, old_links = read_deals()

    for i in range(len(new_titles)):
        if new_titles[i] not in old_titles and new_links[i] not in old_links:
            new_deals.append({"title":new_titles[i],"link":new_links[i]})

    return new_deals

        



            

