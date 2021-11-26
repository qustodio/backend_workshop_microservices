from locust import HttpUser, task


class CatalogUser(HttpUser):
    @task
    def get_catalog(self):
        self.client.get('/catalogs/books')

    @task
    def get_books(self):
        for i in range(4):
            self.client.get(f'/catalogs/books/{i+1}')

    @task
    def get_authors(self):
        self.client.get('/catalogs/authors')
