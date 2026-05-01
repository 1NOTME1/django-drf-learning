from rest_framework.test import APITestCase
from .models import UserProfile


class UserListApiTest(APITestCase):
    def test_users_list_returns_200(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, 200)

    def test_users_list_invalid_is_active_returns_400(self):
        response = self.client.get("/api/users/?is_active=yes")
        self.assertEqual(response.status_code, 400)

    def test_users_list_valid_min_age_returns_200(self):
        response = self.client.get("/api/users/?min_age=18")
        self.assertEqual(response.status_code, 200)

    def test_users_list_min_age_filters_users(self):
        UserProfile.objects.create(
            name="Jan",
            age=17,
            is_active=True,
        )

        UserProfile.objects.create(
            name="Anna",
            age=25,
            is_active=True,
        )

        response = self.client.get("/api/users/?min_age=18")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["data"][0]["name"], "Anna")

    def test_users_list_invalid_min_age_returns_400(self):
        response = self.client.get("/api/users/?min_age=abc")
        self.assertEqual(response.status_code, 400)
    
    def test_users_list_empty_min_age_returns_400(self):
        response = self.client.get("/api/users/?min_age=")
        self.assertEqual(response.status_code, 400)

    def test_users_list_invalid_ordering_returns_400(self):
        response = self.client.get("/api/users/?ordering=email")
        self.assertEqual(response.status_code, 400)