import unittest
import warnings
from finalapi import app


class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), """
    North Wind Customers CRUD

    SELECT OPERATION
    [1] Add Customers
    [2] Retrieve Customers
    [3] Update Customers
    [4] Delete Customers
    [E] Exit
    """)
    #get functions
    def test_customers(self):
        response = self.app.get("/customers")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Bedecs" in response.data.decode())

    def test_getcustomers_by_id(self):
        response = self.app.get("/customers/12")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Edwards" in response.data.decode())

    def test_get_customer_by_id_not_found(self):
        response = self.app.get(f"/customers/69")
        self.assertEqual(response.status_code, 404) 

    def test_getcustomers_by_order(self):
        response = self.app.get("/customers/29/orders")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Lee" in response.data.decode()) 
    
    def test_get_customer_orders_not_found(self):
        response = self.app.get(f"/customers/69/orders")
        self.assertEqual(response.status_code, 404)

    def test_getcustomers_by_city(self):
        response = self.app.get("/customers/'denver'")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Grilo" in response.data.decode())
    
    def test_get_customers_by_city_not_found(self):
        city = "Atlantis City"
        response = self.app.get(f"/customers/{city}")
        self.assertEqual(response.status_code, 404) 

    def test_add_customer(self):
        data = {
            "company": "Company TUV",
            "first_name": "Gyutaro",
            "last_name": "Momoshiki",
            "job_title": "Purcahsing Assistant",
            "address": "123 69th Street",
            "city": "New Jersey"
        }
        response = self.app.post("/customers", json=data)
        self.assertEqual(response.status_code, 201)

    def test_update_customer(self):
        data = {
            "company": "Company ZXC",
            "first_name": "Gamaboko",
            "last_name": "Gonpachiro",
            "job_title": "Purchasing Manager",
            "address": "345 12th Street",
            "city": "Denver"
        }
        response = self.app.put("/customers/36", json=data)
        self.assertEqual(response.status_code, 201)

    def test_update_customer_non_existing(self):
        data = {
            "company": "Company ZXC",
            "first_name": "Gamaboko",
            "last_name": "Gonpachiro",
            "job_title": "Purchasing Manager",
            "address": "345 12th Street",
            "city": "Denver"
        }
        response = self.app.put("/customers/36", json=data)
        self.assertEqual(response.status_code, 201)
    
    def test_delete_customer(self):
        response = self.app.delete("/customers/48")
        self.assertEqual(response.status_code, 200)

    def test_delete_customer_non_existing(self):
        response = self.app.delete("/customers/999")
        self.assertEqual(response.status_code, 404)  # HTTP 404 Not Found
        self.assertEqual(response.json, "Customer 999 does not exist")
     


if __name__ == "__main__":
    unittest.main()