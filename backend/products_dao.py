from sqlconnection import get_sql_connection
import logging
def get_all_products(connection):


    cursor = connection.cursor()
    query = (
        "SELECT products.product_id, products.name, products.uom_id, products.price_per_unit,uom.uom_name FROM products inner join uom on products.uom_id=uom.uom_id;")
    cursor.execute(query)
    response = []
    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append(
            {
                'product_id': product_id,
                'name': name,
                'uom_id': uom_id,
                'price_per_unit': price_per_unit,
                'uom_name': uom_name
            }
        )

    return response

def insert_new_product(connection, product):
    try:
        cursor = connection.cursor()
        query = ("INSERT INTO products "
                 "(name, uom_id, price_per_unit) "
                 "values (%s, %s, %s)")
        data = (product['product_name'], product['uom_id'], product['price_per_unit'])
        cursor.execute(query, data)
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        logging.error("Error inserting product: %s", e)
        raise

def edit_product(connection, product_id, new_product_data):
    try:
        cursor = connection.cursor()
        query = ("UPDATE products SET "
                 "name = %s, "
                 "uom_id = %s, "
                 "price_per_unit = %s "
                 "WHERE product_id = %s")
        data = (new_product_data['product_name'], new_product_data['uom_id'], new_product_data['price_per_unit'], product_id)
        cursor.execute(query, data)
        connection.commit()
        return product_id
    except Exception as e:
        logging.error("Error editing product: %s", e)
        raise



def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = ("DELETE FROM products where product_id=" + str(product_id))
    cursor.execute(query)
    connection.commit()

if __name__=='__main__':
    connection= get_sql_connection()
    print(insert_new_product(connection, {
        'product_name': 'cabbage',
        'uom_id': '1',
        'price_per_unit': '10'
    }))
    print(delete_product(connection,19))