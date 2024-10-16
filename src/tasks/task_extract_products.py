import requests
from bs4 import BeautifulSoup
from prefect import task

@task(name="Extraer productos de Sodimac")
def task_extract_products(query):
    url = f"https://www.sodimac.com.pe/sodimac-pe/buscar?Ntt={query}"
    response = requests.get(url)
    html_doc = response.text

    html = BeautifulSoup(html_doc, "html.parser")

    product_list = html.find_all("div", {"class":"jsx-1068418086 search-results-4-grid grid-pod"})
    products = []
    #print(product_list)

    for product in product_list:
        # Nombre del producto
        name_element = product.find("b", class_="jsx-33793501 copy2 primary jsx-3451706699 normal line-clamp line-clamp-3 pod-subTitle subTitle-rebrand")
        #print("nombre: ",name_element)
        product_name = name_element.get_text() if name_element else "Nombre no disponible"
        #print(product_name)

        # Marca
        brand_element = product.find("b", class_="jsx-33793501 title1 secondary jsx-3451706699 bold pod-title title-rebrand")
        #print("marca: ",brand_element)
        brand_name = brand_element.get_text() if brand_element else "Marca no disponible"
        #print(brand_name)
        
        # Precio
        price_element = product.find("span", class_="copy10 primary medium jsx-3451706699 normal line-height-22")
        #print("precio: ",price_element)
        product_price = float(price_element.get_text().strip().replace("S/", "").replace(",", "").replace("\xa0m²","").strip()) if price_element else 0.0
        #print(product_price)

        # Oferta CMR
        cmr_element = product.find("i", class_="jsx-2128016101 unica-cmr-icon pdp-icon")
        #print("CMR: ",cmr_element)
        cmr_sale = cmr_element is not None
        #print(cmr_sale)

        # Precio CMR
        price_cmr_element = product.find("span", class_="copy10 primary high jsx-3451706699 normal line-height-22")
        #print("precio CMR: ",price_cmr_element)
        product_price_cmr = float(price_cmr_element.get_text().strip().replace("S/", "").replace(",", "").replace("\xa0m²","").strip()) if price_cmr_element else None
        #print(product_price_cmr)

        # Precio normal
        regular_price_element = product.find("span", class_="copy3 primary medium jsx-3451706699 normal crossed line-height-17")
        #print("precio normal: ",regular_price_element)
        product_regular_price = float(regular_price_element.get_text().strip().replace("S/", "").replace(",", "").replace("\xa0m²","").strip()) if regular_price_element else product_price
        #print(product_regular_price)

        #Vendedor
        seller_element = product.find("b", class_="jsx-33793501 copy2 primary jsx-3451706699 normal pod-sellerText seller-text-rebrand")
        #print("vendedor: ",seller_element)
        seller_name = seller_element.get_text()[4:] if name_element else "Nombre de vendedor no disponible"
        #print(seller_name)

        # Etiqueta "Llega mañana"
        shipping_info = product.find("span", class_="jsx-3167696911 jsx-2485730994 copy8 primary jsx-3451706699 bold pod-badges-item-4_GRID pod-badges-item")
        #print("llega mañana: ",shipping_info)
        arrives_tomorrow = "Llega mañana" in shipping_info.get_text() if shipping_info else False
        #print(arrives_tomorrow)

        # Descuento
        discount_info = product.find("span",class_="jsx-2855665538 copy5 primary jsx-3451706699 bold discount-badge-item")
        #print("descuento: ",discount_info)
        product_discount = int(discount_info.get_text()[1:-1]) if discount_info else 0
        #print(product_discount)

        # Calificación
        rating_info = product.find("div", class_="jsx-1982392636 ratings")
        #print("puntaje: ",rating_info)
        product_rating = float(rating_info["data-rating"]) if rating_info and "data-rating" in rating_info.attrs else 0.0
        #print(product_rating)

        # Número de calificaciones
        reviews_info = product.find("span", class_="jsx-2146889120 reviewCount reviewCount-4_GRID")
        #print("reseñas: ",reviews_info)
        product_reviews = int(reviews_info.get_text()[1:-1]) if reviews_info else 0
        #print(product_reviews)

        #print(product_name,",",brand_name,",", product_price,",",cmr_sale,",",product_price_cmr,",",product_regular_price,",",arrives_tomorrow,",",product_discount,",",product_rating,",",product_reviews)

        # Oferta única CMR
        products.append((
            product_name,
            brand_name, 
            product_price,
            cmr_sale,
            product_price_cmr,
            product_regular_price,
            seller_name,
            arrives_tomorrow,
            product_discount,
            product_rating,
            product_reviews
        ))
    return products