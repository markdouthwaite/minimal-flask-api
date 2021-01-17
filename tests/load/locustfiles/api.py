from locust import task, between, HttpUser


class DefaultUser(HttpUser):

    # wait between requests from one user for between 1 and 5 seconds.
    wait_time = between(1, 5)

    @task
    def index(self):
        self.client.get("/")

    @task
    def check_health(self):
        with self.client.get("/health", catch_response=True) as response:
            if response.text != "OK":
                response.failure("Wrong response.")
