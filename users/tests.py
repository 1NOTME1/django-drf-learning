from rest_framework.test import APITestCase
from .models import UserProfile, Department


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

    def test_users_list_ordering_by_age_desc(self):

        UserProfile.objects.create(name="Jan", age=20, is_active=True)

        UserProfile.objects.create(name="Anna", age=35, is_active=True)

        UserProfile.objects.create(name="Kuba", age=25, is_active=True)

        response = self.client.get("/api/users/?ordering=-age")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(response.data["data"][0]["name"], "Anna")
        self.assertEqual(response.data["data"][1]["name"], "Kuba")
        self.assertEqual(response.data["data"][2]["name"], "Jan")

    def test_users_list_filters_is_active_true(self):
        UserProfile.objects.create(name="Jan", age=20, is_active=True)

        UserProfile.objects.create(name="Anna", age=35, is_active=False)

        UserProfile.objects.create(name="Kuba", age=25, is_active=True)

        response = self.client.get("/api/users/?is_active=true")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["data"][0]["name"], "Jan")
        self.assertEqual(response.data["data"][1]["name"], "Kuba")

    def test_users_list_filters_by_name(self):
        UserProfile.objects.create(name="Kamil", age=20, is_active=True)

        UserProfile.objects.create(name="Kasia", age=30, is_active=True)

        UserProfile.objects.create(name="Anna", age=25, is_active=True)

        response = self.client.get("/api/users/?name=ka")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["data"][0]["name"], "Kamil")
        self.assertEqual(response.data["data"][1]["name"], "Kasia")

    def test_users_list_ordering_by_name(self):
        UserProfile.objects.create(name="Kuba", age=25, is_active=True)

        UserProfile.objects.create(name="Anna", age=35, is_active=True)

        UserProfile.objects.create(name="Jan", age=20, is_active=True)

        response = self.client.get("/api/users/?ordering=name")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)

        names = [user["name"] for user in response.data["data"]]
        self.assertEqual(names, ["Anna", "Jan", "Kuba"])

    def test_create_user_valid_data_returns_201(self):
        payload = {
            "name": "Jan",
            "age": 25,
            "is_active": True,
        }

        response = self.client.post("/api/users/create/", payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "ok")
        self.assertEqual(response.data["data"]["name"], "Jan")
        self.assertEqual(response.data["data"]["age"], 25)
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_create_user_empty_name_returns_400(self):
        payload = {"name": "   ", "age": 25, "is_active": True}

        response = self.client.post("/api/users/create/", payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["status"], "error")
        self.assertIn("name", response.data["errors"])
        self.assertEqual(UserProfile.objects.count(), 0)

    def test_create_user_with_department_returns_201(self):
        department = Department.objects.create(name="IT")

        payload = {
            "name": "Jan",
            "age": 25,
            "is_active": True,
            "department": department.id,
        }

        response = self.client.post("/api/users/create/", payload, format="json")
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "ok")
        self.assertEqual(response.data["data"]["department"], department.id)
        self.assertEqual(response.data["data"]["department_name"], "IT")
        self.assertEqual(UserProfile.objects.count(), 1)

        