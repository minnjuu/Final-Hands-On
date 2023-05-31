
from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

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

#index page
@app.route("/")
def home_page():
    return """
    <form action="/customers" method="GET">
        <input type="text" name="query" placeholder="Enter your search query">
        <input type="submit" value="Search">
    </form>
    """

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
    return make_response(jsonify(data), 200)

#customer id
@app.route("/customers/<int:id>", methods=["GET"])
def get_customer_by_id(id):
    query = f"""SELECT id, company,
     first_name, last_name, job_title, address, city FROM customers WHERE id = {id};"""
    data = data_fetch(query)
    if data == []:
        return make_response(jsonify(f"Customer {id} has no record in this table"), 404)
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
    result = {"Customer Id": data[0]['id'], "Customer Name": data[0]['Customer'], "No. of Orders": len(data), "Orders": orders}
    if data == []:
        return make_response(jsonify(f"Customer {id} has no recorded orders"), 404)
    return make_response(jsonify(result), 200)

#customer city
@app.route("/customers/<string:city>", methods = ["GET"])
def get_customers_by_city(city):
    query = f"""SELECT id, company, first_name, last_name, job_title, address, city FROM customers
    WHERE city = {city};"""
    data = data_fetch(query)
    result = {"City": data[0]['city'], "Customer Count": len(data), "List of Customers": data}
    if data == []:
        return make_response(jsonify("No recorded customers for this City"), 404)
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
    return make_response(jsonify({"message":"Customer added successfully"}),201,)

@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):
    query = f""" DELETE FROM customers WHERE id = {id}; """
    data_fetch(query)
    mysql.connection.commit()
    return make_response(jsonify(f"Customer {id} records has been successfully deleted"), 200)


if __name__ == "__main__""":
    app.run(debug=True)