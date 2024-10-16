# Proyecto ETL de Productos de Sodimac

Este proyecto implementa un flujo ETL (Extracción, Transformación y Carga) para extraer información sobre productos del sitio web de **SODIMAC**. Los datos extraídos incluyen el nombre del producto, marca, precio, vendedor, descuento, opción de despacho rápido, calificaciones y número de reseñas, posteriormente estos datos serán cargados en la tabla **product** de la base de datos **sodimac**.

## Datos extraídos
```markdown
-product_name: Nombre del producto
-brand_name: Nombre de la marca
-price: Precio del producto
-cmr_sale: Si tiene ua oferta con tarjeta CMR(True) o no (False)
-product_price_cmr: Precio al pagar con tarjeta CMR, en caso no tenga descuento por cmr, NULL
-regular_price: Precio sin descuento, en caso no exista ningún descuento se mostrará price
-seller: Nombre del vendedor
-arrives_tomorrow: Si está disponible para entrega al día siguiente (True) o no (False)
-discount: Porcentaje de descuento sobre el regular_price
-rating: Puntaje promedio de las calificaciones sobre 5, en caso no haya calificaciones mostrará 0
-reviews: Número de reseñas sobre el producto
```

## Ejemplo
```markdown
-product_name: 'Silla Bar alta giratoria Negro'
-brand_name: 'CASA BONITA'
-price: 149.9
-cmr_sale: 1
-product_price_cmr: 99.9
-regular_price: 149.9
-seller: Sodimac
-arrives_tomorrow: 1
-discount: 33
-rating: 4.5747
-reviews: 388
```