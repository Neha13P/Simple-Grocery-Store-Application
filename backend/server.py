from flask import Flask, request, jsonify
import products_dao
import uom_dao
from sqlconnection import get_sql_connection
import json
import orders_dao
import logging

app = Flask(__name__)

logging.basicConfig(filename='server.log', level=logging.DEBUG)
connection = get_sql_connection()

@app.route('/getProducts', methods=['GET'])
def get_products():
    try:
        products = products_dao.get_all_products(connection)
        logging.info("Product data fetched successfully")
        response = jsonify(products)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    except Exception as e:
        logging.error("Error fetching product data: %s", e)
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-control-Allow-origin', '*')
    return response


@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({'product_id': return_id})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add("Access-control-Allow-origin", '*')
    return response


@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({'product_id': product_id})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/editProduct', methods=['POST'])
def edit_product():
    try:
        request_payload = json.loads(request.form['data'])
        product_id = request_payload['product_id']
        new_product_data = request_payload['new_product_data']

        # Update the product details in the database
        updated_product_id = products_dao.edit_product(connection, product_id, new_product_data)

        response = jsonify({'product_id': updated_product_id})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    except Exception as e:
        logging.error("Error editing product: %s", e)
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == "__main__":
    print('Starting Python Flask For Grocery Store Management System')
    app.run(port=5000)