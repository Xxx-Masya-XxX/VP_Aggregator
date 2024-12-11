import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json

def parse_vapoint():
    url = "https://vapoint.ru/"
    response = requests.get(url)  
    if response.status_code != 200:
        return {"error": "Не удалось получить данные с сайта"}
    soup = BeautifulSoup(response.content, "html.parser")
    catalog_div = soup.find("div", class_="Catalog_products__HQX3Q")
    product_cards = catalog_div.find_all("div", class_="ProductCard_container__cdrf0")
    result = {}

    for idx, product_card in enumerate(product_cards, 1):
        h4 = product_card.find("h4")
        h3 = product_card.find("h3")
    
        if h4 and h3:
            h4_text = h4.text
            currency_amount = ''.join(filter(str.isdigit, h4_text))
            currency_amount = int(currency_amount) if currency_amount else 0
            h3_text = h3.text
            price = ''.join(filter(str.isdigit, h3_text))
            price = int(price) if price else 0
            result[idx] = {
                "vp": currency_amount,
                "price": price,
                "site": url
            }
    return result


def parse_vpsale():
    url = "https://vpsale.ru/"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Не удалось получить данные с сайта"}
    soup = BeautifulSoup(response.content, "html.parser")
    catalog_div = soup.find("div", class_="main-catalog")
    product_cards = catalog_div.find_all("div", class_="product_card")
    result = {}
    for idx, product_card in enumerate(product_cards, 1):
        h4 = product_card.find("span",class_="product_card_count")
        h3 = product_card.find("span",class_="product_card_cost")
        if h4 and h3:
            h4_text = h4.text
            currency_amount = ''.join(filter(str.isdigit, h4_text))
            currency_amount = int(currency_amount) if currency_amount else 0
            h3_text = h3.text
            price = ''.join(filter(str.isdigit, h3_text))
            price = int(price) if price else 0
            result[idx] = {
                "vp": currency_amount,
                "price": price,
                "site": url
            }
    return result


def merge_vp_data(*args):
    merged_data = {}
    current_offset = 0
    for data in args:
        for key, value in data.items():
            merged_data[current_offset + key] = value
        current_offset += len(data)
    return merged_data

if __name__ == "__main__":
    data = merge_vp_data(
        parse_vapoint(),
        parse_vpsale()
    )
    with open('merged_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    pprint(data)
