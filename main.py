import pandas as pd
from bs4 import BeautifulSoup as bs
import requests


def search_term(term):
    url = f"https://lista.mercadolivre.com.br/{term}#D[A:{term}]"
    return url

# This function is the responsible for analyzing the HTML of the sit.
def item_informations(item): 
    # Find the item's title.
    exist_title  = item.find('h2', class_ = "ui-search-item__title")
    if exist_title:
        title = exist_title.text
    else:
        title = "None"

    # Finde the item's price.
    price_integer = item.find('span', class_ = "andes-money-amount__fraction").text
    find_cents = item.find('span', class_ = "andes-money-amount__cents andes-money-amount__cents--superscript-24")
    if find_cents:
        price = price_integer + ',' + find_cents.text
    else:
        price = price_integer + ',' + '00'

    # Find the item's rating value.
    try:
        rating = item.find('span', class_ = 'ui-search-reviews__rating-number').text
    except AttributeError:
        rating = "None"

    #Find the item's quantity of reviews of the item.
    try:
        reviews = item.find('span', class_ = 'ui-search-reviews__amount').text
    except AttributeError:
        reviews = "None"

    informations = (title, price, rating, reviews)

    # Return a tuple with all the informations we got.
    return informations

# This is the function responsible for making the request.
# Also, this function turn the result into a panda table.
def get_doc(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    page = requests.get(url, headers=headers)
    soup = bs(page.content, "html.parser")

    records = []

    # Find the HTML element that contains all the products.
    results = soup.find_all("ol", attrs={'class': 'ui-search-layout ui-search-layout--grid'})
    for item in results:
        record = item_informations(item)
        if record:
            records.append(record)

    df = pd.DataFrame(records, columns=['Title', 'Price', 'Rating', 'Reviews'])
    return df


site = search_term('mala')
print(get_doc(site))

    
