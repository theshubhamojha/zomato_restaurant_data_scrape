import requests
from bs4 import BeautifulSoup
import pandas
import csv
import re

agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
page_no = 1
list_restaurants =[]
base_url = "https://www.zomato.com/bangalore/south-bangalore-restaurants"
number_of_restaurants = 0

for page in range(0,6):
    print("Scrapping page number " + str(page_no) + "...")

    response = requests.get(base_url + "?page={0}".format(page_no), headers=agent)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    search_results = soup.find_all("div", {'id': 'orig-search-list'})
    list_of_contents = search_results[0].find_all("div", {'class': 'content'})

    
    for i in range(0,15):

        name = list_of_contents[i].find("a", {'data-result-type': 'ResCard_Name'})
        area = list_of_contents[i].find("b")
        ratings = list_of_contents[i].find("div", {'data-variation': 'mini inverted'})

        rest6 = list_of_contents[i].find_all("div", {'class': 'search-page-text clearfix row'})
        rest7 = rest6[0].find_all("span", {'class': 'col-s-11 col-m-12 nowrap pl0'})
        rest8 = rest7[0].find_all("a")

        restaurant_type = [e.string for e in rest8]
        votes = list_of_contents[i].find("span", {'class': re.compile(r'rating-votes-div*')})

        if votes is None:
            continue

        dataframe ={}
        dataframe["serial_number"] = number_of_restaurants+1
        dataframe["name"] = name.string.replace('\n', ' ').strip()
        dataframe["area"] = area.string.replace('\n', ' ').strip()
        dataframe["rating"] = ratings.string.replace('\n', ' ').strip()
        dataframe["restaurant_type"] = restaurant_type
        dataframe["votes"] = votes.string.split()[0].strip()
        list_restaurants.append(dataframe)

        number_of_restaurants = number_of_restaurants + 1
        if number_of_restaurants == 80:
            break

    page_no += 1
    
df = pandas.DataFrame(list_restaurants)
df.to_csv("zomato_restaurants.csv")
df.to_json("zomato_restaurants.json", orient='records')