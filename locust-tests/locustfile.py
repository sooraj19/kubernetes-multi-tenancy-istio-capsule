from locust import HttpUser, task

class MultiTenantUser(HttpUser):
    @task
    def make_request(self):
        self.client.get("/tenant1")
        self.client.get("/tenant2")