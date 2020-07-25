import engine
import argparse


parser = argparse.ArgumentParser(description="Displays new job offers on webtrh.cz")
parser.add_argument("-s","--show", type=int, metavar='',nargs='?', const=10000, help="displays new job offers")
parser.add_argument("-m","--mark", action="store_true",help="marks all job offers as readed")
parser.add_argument('-c','--count', action="store_true", help="prints count of new job offers")
args = parser.parse_args()



if __name__ == "__main__":
    if args.show:
        new_deals = engine.get_new_deals()
        if len(new_deals) == 0:
                print("Nenalezl jsem žádné nové zakázky")
        else:
            if args.show == 10000:    
                for index,deal in enumerate(new_deals):
                    print("\n")
                    print(index + 1)
                    print(deal["title"])
                    print(deal["link"])
            else:
                if args.show - 1 < len(new_deals):
                    deal = new_deals[args.show -1]
                    article, budget, numbers = engine.get_deal_details(deal['link'])
                    print(deal['title'] + "\n")
                    print(budget + "\n")
                    print(numbers + "\n")
                    print(article + "\n")
                    print(deal['link'])
                else:
                    print(f'Vybrat můžeš pouze zakázky 1 - {len(new_deals)}')
        
    if args.mark:
        engine.write_deals()
    if args.count:
        print(f"Počet nových zakázek: {len(engine.get_new_deals())}")