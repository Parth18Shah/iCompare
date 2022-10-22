import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

def flipkart_scraping(product):
    print(product)
    try:
        flipkart_base_url = "https://www.flipkart.com/search?q="

        try:
            product_name = product.replace(" ", "+")
            flipkart_url = flipkart_base_url + product_name
        except:
            print("No search found :")
            return None 

        #print(flipkart_url)

        headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}

        flipkart_site = requests.get(flipkart_url, headers= headers)

        flipkart_soup = BeautifulSoup(flipkart_site.text, "html.parser")

        try:
            name = flipkart_soup.find("div",class_='_4rR01T').text
            price = int(flipkart_soup.find("div", class_="_30jeq3 _1_WHN1").text[1:].replace(',', ""))
            description = list(flipkart_soup.find("ul", class_='_1xgFaf').children)
        except:
            try :
                product_link = flipkart_soup.find("a",class_='_1fQZEK')["href"]
                product_url = "https://www.flipkart.com" + product_link

                #print(product_url)

                product_site = requests.get(product_url, headers=headers)

                product_soup = BeautifulSoup(product_site.text, "html.parser")

                name = product_soup.find("span", class_='B_NuCI').text
                price = int(product_soup.find("div", class_="_30jeq3 _16Jk6d").text[1:].replace(',', ""))
                description = product_soup.find_all("li", class_='_21Ahn-')
            except :
                print("The product entered cannot be found :")
                return None
                # exit()

        # print("\nName :  ",name)
        # print("\nPrice : ",price)
        # print("\nDescription : ")
        product_des = []
        for des in description:
            # print("        ",des.text)
            product_des.append(des.text)

        data = {"name":name,"price":price,"description":product_des}
        return data
    except:
        return None



# data_path = r"C:\Users\Owner\Desktop\MIP_project\prices_data"
# products = {'iphone 8 64GB' : r'\iphone_8_64GB.csv',
#             'iphone 8 plus 64GB' : r'\iphone_8_PLUS_64GB.csv',
#             'iphone XR 64GB' : r'\iphone_XR_64GB.csv',
#             'iphone X 64GB' : r'\iphone_X_64GB.csv', 
#             'iphone XS MAX 64GB' : r'\iphone_XS_MAX_64GB.csv',
#             'iphone XS MAX 512GB' : r'\iphone_XS_MAX_512GB.csv',
#             'iphone 11 64GB' : r'\iphone_11_64GB.csv',
#             'iphone 11 128GB' : r'\iphone_11_128GB.csv',
#             'iphone 11 pro 64GB' : r'\iphone_11_PRO_64GB.csv',
#             'iphone 11 pro 256GB' : r'\iphone_11_PRO_256GB.csv',
#             'iphone 11 pro 512GB' : r'\iphone_11_PRO_512GB.csv',
#             'iphone 11 pro max 64GB' : r'\iphone_11_PRO_MAX_64GB.csv',
#             'iphone 11 pro max 256GB' : r'\iphone_11_PRO_MAX_256GB.csv',
#             'apple airpods' : r'\apple_airpods.csv',
#             }

# filename = data_path + products['iphone 8 64GB']

# today = date.today()
# date_format = today.strftime("%d/%m/%Y")
# with open(filename, 'a', newline='') as csvfile:
#      filewriter = csv.writer(csvfile, delimiter=',')
#      filewriter.writerow([date_format,price])