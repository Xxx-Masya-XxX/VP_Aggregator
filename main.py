from parse_sites import merge_vp_data,parse_vapoint,parse_vpsale
import json
from itertools import combinations_with_replacement


def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def generate_combinations(products, max_price):
    product_items = list(products.items())
    all_combinations = []
    for r in range(1, 6):
        for combo in combinations_with_replacement(product_items, r):
            total_vp = sum(item[1]['vp'] for item in combo)
            total_price = sum(item[1]['price'] for item in combo)
            if total_price <= max_price:
                all_combinations.append({
                    "combination": [{'vp':item[1]['vp'], 'price':item[1]['price'], 'site':item[1]['site']} for item in combo],
                    "total_vp": total_vp,
                    "total_price": total_price
                })
    return all_combinations

def find_combo(combinations_list, target_vp):
    for combo in combinations_list:
        if combo['total_vp'] >= target_vp:
            return combo
    return None

def filter_by_price(combinations_list):
    unique_combinations = {}
    for combo in combinations_list:
        total_vp = combo['total_vp']
        total_price = combo['total_price']
        if total_vp not in unique_combinations or total_price < unique_combinations[total_vp]['total_price']:
            unique_combinations[total_vp] = combo
    return list(unique_combinations.values())

if __name__ == "__main__":
    data = merge_vp_data(
        parse_vapoint(),
        parse_vpsale()
    )
    with open('merged_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    products = load_data('merged_data.json')
    max_price = 15000
    combinations_list = generate_combinations(products, max_price)
    combinations_list.sort(key=lambda x: x['total_vp'])
    
    ff = filter_by_price(combinations_list)
    print(f"Всего найдено комбинаций: {len(ff)}")
    
    target_vp = 1075
    result = find_combo(ff, target_vp)
    print(f"Результат: {result}")

    with open("ddata.json","w", encoding='utf-8') as f:
        json.dump(ff, f, ensure_ascii=False, indent=4)
