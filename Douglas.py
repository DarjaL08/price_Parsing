import requests
from bs4 import BeautifulSoup

def clean_text(text):
    return ''.join(char for char in text if char.isalnum() or char.isspace())

def get_price_douglas(brand, product):
    output_file = "douglas_results.txt"
    results = []

    url = f"https://www.douglas.lv/lv/{brand}/" 
    response = requests.get(url)

    if response.status_code != 200:
        result = {"name": None, "price": f"Could not load {url}. Code: {response.status_code}"}
        results.append(result)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"{result['price']}\n")
        return results


    soup = BeautifulSoup(response.text, "html.parser")
    product_cleaned = clean_text(product.lower().strip())

    
    products = soup.find_all("div", class_="product_element lv") 
    if not products:
        result = {"name": None, "price": f"Could not find the searched information for '{brand}'"}
        results.append(result)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"{result['price']}\n")
        return results

    
    for item in products:
        name_tag = item.find("span", class_="name") 
        price_tag = item.find("span", class_="price")  
        if name_tag and price_tag:
            name_text = name_tag.get_text(strip=True)
            name_text_cleaned = clean_text(name_text.lower())
            if product_cleaned in name_text_cleaned:
                result = {"name": name_text, "price": price_tag.get_text(strip=True)}
                results.append(result)

    
    if not results:
        result = {"name": None, "price": f"The searched product '{product}' wasn't found on the page"}
        results.append(result)

    
    with open(output_file, "w", encoding="utf-8") as f:
        for result in results:
            if result["name"]:
                f.write(f"Found: {result['name']}, Price: {result['price']}\n")
            else:
                f.write(f"{result['price']}\n")
    
    return results

if __name__ == "__main__":
    
    brand = input("Enter brand name, please: ")
    product = input("Enter the title of the product, please: ")
    
    
    results = get_price_douglas(brand, product)
    
    for result in results:
        if result["name"]:
            print(f"Found: {result['name']}, Price: {result['price']}")
        else:
            print(f"Error: {result['price']}")
