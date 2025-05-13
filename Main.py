from Kristers import get_price_kristers
from Douglas import get_price_douglas

def compare_prices(kristers_info, douglas_info):
    if not kristers_info and not douglas_info:
        print("The searched product wasn't found anywhere.")
        return
    
    found_valid = False
    for k_item in kristers_info:
        k_name = k_item.get("name")
        k_price = k_item.get("price")
        
        # Пропускаем элементы с name=None или некорректной ценой
        if not k_name or "Error" in k_price:
            continue
        
        found_valid = True
        print(f"\nKsisters: {k_name}, Price: {k_price}")
        
        for d_item in douglas_info:
            d_name = d_item.get("name")
            d_price = d_item.get("price")
            
            # Пропускаем элементы с name=None или некорректной ценой
            if not d_name or "Error" in d_price:
                continue
                
            if k_name.lower() in d_name.lower() or d_name.lower() in k_name.lower():
                print(f"Douglas: {d_name}, price: {d_price}")
                try:
                    k_price_val = float(k_price.replace("€", "").replace(",", ".").strip())
                    d_price_val = float(d_price.replace("€", "").replace(",", ".").strip())
                    if k_price_val < d_price_val:
                        print(f"Ksisters has lower price in difference of {d_price_val - k_price_val:.2f}€")
                    elif k_price_val > d_price_val:
                        print(f"Douglas has lower price in difference of {k_price_val - d_price_val:.2f}€")
                    else:
                        print("Prices are equal")
                except ValueError:
                    print("Could not find the price in the searched format")
                break
        else:
            print("Could not find the same product on Douglas.")
    
    if not found_valid:
        print("Could not find the product on Ksisters.")

def main():
    brand = input("Enter brand name, please: ")
    product = input("Enter the title of the product, please: ")

    # Переменные для хранения результатов
    kristers_info = []
    douglas_info = []

    # Запуск парсинга для ksisters.lv
    try:
        kristers_results = get_price_kristers(brand, product)
        kristers_info = kristers_results
        for item in kristers_info:
            if item.get("name"):  # Выводим только успешные результаты
                print(f"Found: {item['name']}, Price: {item['price']}")
            else:
                print(f"Error: {item['price']}")
    except Exception as e:
        print(f"An error occured for ksisters.lv: {e}")

    # Запуск парсинга для douglas.lv
    try:
        douglas_results = get_price_douglas(brand, product)
        douglas_info = douglas_results
        for item in douglas_info:
            if item.get("name"):  # Выводим только успешные результаты
                print(f"Found: {item['name']}, Price: {item['price']}")
            else:
                print(f"Error: {item['price']}")
    except Exception as e:
        print(f"An error occured for douglas.lv: {e}")

    # Сравнение цен
    compare_prices(kristers_info, douglas_info)

if __name__ == "__main__":
    main()