import os
from dotenv import load_dotenv
from mysql import connector
from prefect import task


load_dotenv()
config = {
    "host":"localhost",
    "user":"root",
    "password": os.getenv("DB_PASSWORD"),
}

@task(name="Crear base de datos si no existe")
def create_database():
    try:
        with connector.connect(**config) as db:
            with db.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS sodimac")
                db.commit()
                print("Base de datos 'sodimac' creada o ya existe.")
    except connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")

@task(name="Limpieza tabla productos")
def delete_elements():
	config["database"] = "sodimac"
	with connector.connect(**config) as db:
		with db.cursor() as cursor:
			try: 
				cursor.execute("drop table if exists product")
				db.commit()
			except Exception as error:
				print("Error: ",error)

@task(name="Carga de productos en la bd")
def task_load_products_baseline(products):
	config["database"] = "sodimac"
	with connector.connect(**config) as db:
		with db.cursor() as cursor:
			try: 
				cursor.execute("""
						CREATE TABLE IF NOT EXISTS product(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        product_name VARCHAR(200),
						brand_name VARCHAR(200),
                        price FLOAT,
						cmr_sale BOOL,
						product_price_cmr FLOAT,
						regular_price FLOAT,
						seller VARCHAR(50),
                        arrives_tomorrow BOOL,
                        discount INT,
                        rating FLOAT,
                        reviews INT
                    )
				""")
				db.commit()
			except Exception as error:
				print("error: ", error)


			query_insert = """
				INSERT INTO product(product_name, brand_name, price, cmr_sale, product_price_cmr,regular_price, seller,arrives_tomorrow, discount, rating, reviews)
                VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)
			"""
			try:
				cursor.executemany(query_insert, products)
				db.commit()
			except Exception as error:
				print("error: ", error)
				
@task(name="Cargar nuevos productos en la bd")
def task_load_products_update(products):
	with connector.connect(**config) as db:
		with db.cursor() as cursor:
			query_insert = """
				INSERT INTO product(product_name, brand_name, price, cmr_sale, product_price_cmr, regular_price, seller, arrives_tomorrow, discount, rating, reviews)
                VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)
			"""
			for product in products:
				try:
					cursor.execute(query_insert, product)
				except Exception as error:
					print("error: ", error)