
from flask import Flask, make_response, jsonify, request, Response
from flask_mysqldb import MySQL
import xml.etree.ElementTree as ET
import xml.dom.minidom
import re

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "seagate"
app.config["MYSQL_DB"] = "northwind"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

#data fetcher
def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    # Convert bytes to strings
    data = [{k: v.decode() if isinstance(v, bytes) else v for k, v in item.items()} for item in data]
    return data

import xml.dom.minidom

def generate_xml_response(data_list, root_element="root"):
    root = ET.Element(root_element)
    for data in data_list:
        element = ET.SubElement(root, "customer")
        for key, value in data.items():
            sub_element = ET.SubElement(element, key)
            sub_element.text = str(value)
    
    xml_string = ET.tostring(root, encoding='utf-8', method='xml')
    readable_xml = xml.dom.minidom.parseString(xml_string).toprettyxml(indent="  ")
    
    return readable_xml




#index page
@app.route("/")
def home_page():
    return Response("""
    North Wind Customers CRUD

    SELECT OPERATION
    [1] Add Customers
    [2] Retrieve Customers
    [3] Update Customers
    [4] Delete Customers
    [E] Exit
    """, mimetype="text/plain")

#error handler
'''
@app.errorhandler(404)
def not_found_error(error):
    return True
'''

#all customers
@app.route("/customers", methods=["GET"])
def get_customers():
    query = """SELECT id, company,  first_name, last_name, job_title, address, city FROM customers;"""
    data = data_fetch(query)
    format_param = request.args.get('format')

    if format_param == 'xml':
        response = generate_xml_response(data, root_element="Customers")
        return Response(response, content_type='application/xml')
    else:
        return make_response(jsonify(data), 200)

#customer id
@app.route("/customers/<int:id>", methods=["GET"])
def get_customer_by_id(id):
    query = f"""SELECT id, company,
     first_name, last_name, job_title, address, city FROM customers WHERE id = {id};"""
    data = data_fetch(query)
    if data == []:
        return make_response(jsonify(f"Customer {id} has no record in this table"), 404)

    format_param = request.args.get('format')
    if format_param == 'xml':
        response = generate_xml_response(data, root_element="Customer")
        return Response(response, content_type='application/xml')
    else:
        return make_response(jsonify(data), 200)

#customer orders
@app.route("/customers/<int:id>/orders", methods = ["GET"])
def get_customer_orders(id):
    query = f"""SELECT customers.id, 
concat(customers.first_name, " ", customers.last_name) as "Customer",
orders.order_date, 
products.product_name
FROM products
INNER JOIN order_details
ON products.id = order_details.product_id
INNER JOIN orders
ON order_details.order_id = orders.id
INNER JOIN customers
ON orders.customer_id = customers.id
WHERE customer_id = {id}
ORDER by orders.order_date;"""
    data = data_fetch(query)
    orders = [{"product_name": item["product_name"],"order_date": item["order_date"]} for item in data]
    if data == [] and orders == []:
        return make_response(jsonify(f"Customer {id} has no recorded orders"), 404)

    result = {"Customer Id": data[0]['id'], "Customer Name": data[0]['Customer'], "No. of Orders": len(data), "Orders": orders}
    format_param = request.args.get('format')
    if format_param == 'xml':
        response = generate_xml_response(data, root_element="Orders")
        return Response(response, content_type='application/xml')
    return make_response(jsonify(result), 200)

#customer city
@app.route("/customers/<string:city>", methods = ["GET"])
def get_customers_by_city(city):
    query = f"""SELECT id, company, first_name, last_name, job_title, address, city FROM customers
    WHERE city = {city};"""
    data = data_fetch(query)
    if data == []:
        return make_response(jsonify("No recorded customers for this City"), 404)
    
    format_param = request.args.get('format')
    if format_param == 'xml':
        response = generate_xml_response(data, root_element="City")
        return Response(response, content_type='application/xml')
    result = {"City": data[0]['city'], "Customer Count": len(data), "List of Customers": data}
    return make_response(jsonify(result), 200)

@app.route("/customers", methods=["POST"])
def add_customer():
    info = request.get_json()
    company = info["company"]
    first_name = info["first_name"]
    last_name = info["last_name"]
    job_title = info["job_title"]
    address = info["address"]
    city = info["city"]

    query = f"""INSERT INTO customers (company, first_name, last_name, job_title, address, city)
            VALUES ('{company}', '{first_name}', '{last_name}', '{job_title}', '{address}', '{city}')"""

    data = data_fetch(query)
    mysql.connection.commit()
    return make_response(jsonify("Customer added successfully"),201,)

@app.route("/customers/<int:id>", methods=["PUT"])
def update_customer(id):
    info = request.get_json()
    company = info["company"]
    first_name = info["first_name"]
    last_name = info["last_name"]
    job_title = info["job_title"]
    address = info["address"]
    city = info["city"]

    # Check if the customer with the given ID exists
    check_query = f"SELECT * FROM customers WHERE id = {id}"
    existing_customer = data_fetch(check_query)
    if not existing_customer:
        return make_response(jsonify(f"Customer {id} does not exist"), 404)

    query = f"""UPDATE customers
            SET company = '{company}', 
            first_name = '{first_name}', 
            last_name = '{last_name}', 
            job_title = '{job_title}', 
            address = '{address}', 
            city = '{city}'
            WHERE id = {id};"""

    data_fetch(query)
    mysql.connection.commit()
    return make_response(jsonify(f"Customer {id} records have been successfully updated"), 201)


@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):
    check_query = f"SELECT * FROM customers WHERE id = {id}"
    existing_customer = data_fetch(check_query)
    if not existing_customer:
        return make_response(jsonify(f"Customer {id} does not exist"), 404)

    query = f""" DELETE FROM customers WHERE id = {id}; """
    data_fetch(query)
    mysql.connection.commit()
    return make_response(jsonify(f"Customer {id} records has been successfully deleted"), 200)


if __name__ == "__main__""":
    app.run(debug=True)