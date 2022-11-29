""" Performance testing using locust utility for browsing products """
from random import randint
from locust import HttpUser, task, between

""" Note: Locust didn't work on 127.0.0.1:8089 nor 0.0.0.0:8089, it only worked on localhost:8089 domain """


class StorefrontUser(HttpUser):
    """ Perform performance test for viewing products, particular product and adding products to a cart """

    # Delay the time of execution of the tasks between 1-5 seconds and prioritize task weight using random values
    wait_time = between(1, 5)

    @task(2)
    def view_products(self):
        # Randomize the choice of collection id and pass it to the client with the endpoint name
        collection_id = randint(2, 6)
        self.client.get(f"/store/products/?collection_id={collection_id}", name="/store/products/")

    @task(4)
    def view_product(self):
        # Randomize the choice of product id
        product_id = randint(1, 1000)
        self.client.get(f"/store/products/{product_id}", name="/store/products/:id")

    @task(1)
    def add_to_cart(self):
        # Get cart id from on start method provided when the user start browsing the website
        product_id = randint(1, 10)
        self.client.post(f"/store/carts/{self.cart_id}/items/", name="/store/carts/items",
                         json={"product_id": product_id, "quantity": 1})

    @task
    def delay_response(self):
        self.client.get("/playground/delay-response/")


    def on_start(self):
        # Define on start method to get the initiated cart id and use it in add to cart task
        response = self.client.post("/store/carts/")
        result = response.json()
        self.cart_id = result["id"]


