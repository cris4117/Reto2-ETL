from prefect import flow
from tasks.task_extract_products import task_extract_products
from tasks.task_load_products import task_load_products_baseline,task_load_products_update,create_database,delete_elements

TYPE_TASK="baseline"

@flow(name="ETL Productos")
def main_flow():
    search=["silla","piso","juego+de+ollas+20+piezas"]
    create_database()
    delete_elements()
    for query in search:
        products=task_extract_products(query)
        if TYPE_TASK=="baseline":
            task_load_products_baseline(products)
        elif TYPE_TASK=="update":
            task_load_products_update(products)
        # for product in products:
        #     print(product)
if __name__=="__main__":
    main_flow()