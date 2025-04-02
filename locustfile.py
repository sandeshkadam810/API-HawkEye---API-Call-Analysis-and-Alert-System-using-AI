from locust import HttpUser, task, between

class APITestUser(HttpUser):
    wait_time = between(1, 3)  # Random wait time between requests

    @task
    def call_aggregator(self):
        self.client.get("/aggregate")

