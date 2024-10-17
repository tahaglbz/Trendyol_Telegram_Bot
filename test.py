import requests as rq
from bs4 import BeautifulSoup

while True:
    #EX
    url = "https://www.trendyol.com/apple/iphone-16-256gb-laciverttas-p-857296137?boutiqueId=638145&merchantId=968"

    page = rq.get(url)

    html_page = BeautifulSoup(page.content,"html.parser")

    title = html_page.find("h1", class_="pr-new-br").getText()
    latest_price = html_page.find("span", class_="prc-dsc").getText()



    print(title)

    print("Latest Price "+latest_price)
    
    
    

    #telegram part

    import time

    api = "https://api.telegram.org/botYOUR_BOT_TOKEN/SendMessage"

    message = title + "\n" + latest_price

    rq.post(url=api,data={"chat_id":"YOUR_CHAT_ID","text":message}).json()

    time.sleep(86400)


