
from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "seagate"
app.config["MYSQL_DB"] = "northwind"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    # Convert bytes to strings
    data = [{k: v.decode() if isinstance(v, bytes) else v for k, v in item.items()} for item in data]
    return data


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



@app.route("/customers", methods=["GET"])
def get_customers():
    cur = mysql.connection.cursor()
    query = """select * from customers;"""
    cur.execute(query)
    data = data_fetch(query)
    cur.close()
    return make_response(jsonify(data), 200)


if __name__ == "__main__":
    app.run(debug=True)