import requests
from bs4 import BeautifulSoup

def amazon_scrapping(product):

    amazon_base_url = "https://www.amazon.in/s?k="

    try:
        product_name = product.replace(" ", "+")
        add = '&ref=nb_sb_noss_2'
        amazon_url = amazon_base_url + product_name 
    except:
        print("No Search found")
        return None

    # print(amazon_url)

    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}

    amazon_site = requests.get(amazon_url, headers=headers)

    # print(amazon_site.text)
    amazon_soup = BeautifulSoup(amazon_site.text, 'html.parser')

    #product_code = amazon_soup.find("div", class_='sg-col-20-of-24')#['data-asin']

    try:
        product_code = amazon_soup.select('div[data-index]')[0]['data-asin']
        if(product_code == ''):
            product_code = amazon_soup.select('div[data-index]')[1]['data-asin']
    except:
        return None

    # print(product_code)

    product_url = "https://www.amazon.in/dp/" + product_code

    #print(product_url)

    product_site = requests.get(product_url, headers=headers)

    product_soup = BeautifulSoup(product_site.text, 'html.parser')

    try :
        name = product_soup.find("span", {'id': 'productTitle'}).text.strip()
        # print(name)
        description = product_soup.find("div", {'id' : 'feature-bullets'}).findChildren("li")
        try:
            price = int(amazon_soup.find("span", class_='a-price-whole').text.replace(',', ''))
        except:
            price = "Currently unavailable"
        
        # print("\nName : ",name)
        # print("\nPrice : ",price)
        # print("\nDescription : \n")
        amazon_des = []
        for des in description:
            # print("         ",des.text.strip())
            amazon_des.append(des.text.strip())

        amazon_data = {"name":name,"price":price,"description":amazon_des}
        return amazon_data

    except :
        print("An error occured")
        return None


# print(amazon_scrapping("iphone 7"))