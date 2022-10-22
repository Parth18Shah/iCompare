import requests
from bs4 import BeautifulSoup

def news_scrapping():
    news_count = 0
    news_title = []
    news_link = []
    news_para = []

    news_site_url = "https://www.cnet.com/apple/"

    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}

    news_site = requests.get(news_site_url, headers= headers)

    news_site_soup = BeautifulSoup(news_site.text, "html.parser")

    all_news = news_site_soup.findAll("div", {"class" : "row asset"})

    i = 0
    while(news_count < 3):

        news_title_scrapped = all_news[i].find("h2").text
        if("apple" in news_title_scrapped.lower() or "iphone" in news_title_scrapped.lower()):
            news_link_scrapped = "https://www.cnet.com" + all_news[i].find("a",class_='imageLinkWrapper')["href"]

            news_site = requests.get(news_link_scrapped, headers= headers)
            news_site_soup = BeautifulSoup(news_site.text, "html.parser")
            second_para = news_site_soup.find("p",class_="speakableTextP2").text
            
            # print("\n",news_content)
            # print(news_link)
            # print(second_para.text)
            news_title.append(news_title_scrapped)
            news_link.append(news_link_scrapped)
            news_para.append(second_para)


            news_count +=1
        i+=1

    data = {"title":news_title,"link":news_link,"content":news_para}
    return data
