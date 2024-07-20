from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse_lazy
from rest_framework import status
from unittest.mock import patch

from rest_framework.test import APITestCase
from weather_app.models import CityCount
from weather_app.serializers import CityCountSerializer


class WeatherTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse_lazy("weather_app:weather")
        self.form_data = {"city": "Moscow"}
        cache.clear()

    @patch("weather_app.services.get_weather_info")
    def test_get_weather_view(self, mock_get_weather_info):
        mock_get_weather_info.return_value = [
            {
                "time": "2024-07-20T12:00",
                "temperature": 25.5,
                "apparent_temperature": 27.0,
                "degree": "°C",
            }
        ]

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "weather.html")
        self.assertIn("form", response.context)
        self.assertNotIn("last_weather", cache)

    @patch("weather_app.views.get_weather_info")
    @patch("django.core.cache.cache.set")
    def test_form_valid(self, mock_cache_set, mock_get_weather_info):
        mock_get_weather_info.return_value = [
            {
                "time": "2024-07-20T12:00",
                "temperature": 25.5,
                "apparent_temperature": 27.0,
                "degree": "°C",
            }
        ]

        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "weather.html")
        self.assertContains(response, "city")

        mock_cache_set.assert_called_with(
            "last_weather",
            {
                "weather_info": [
                    {
                        "time": "2024-07-20T12:00",
                        "temperature": 25.5,
                        "apparent_temperature": 27.0,
                        "degree": "°C",
                    }
                ],
                "city": "Moscow",
            },
        )

        city_count = CityCount.objects.get(city=self.form_data["city"])
        self.assertEqual(city_count.count, 1)


class CityCountAPIViewTests(APITestCase):
    def setUp(self):
        CityCount.objects.create(city="Moscow", count=5)
        CityCount.objects.create(city="Saint Petersburg", count=3)

    def test_get_city_count(self):
        response = self.client.get("/api/city-count/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CityCountSerializer(
            CityCount.objects.all(),
            many=True,
        ).data
        self.assertEqual(response.json(), expected_data)

    def test_get_city_count_empty(self):
        CityCount.objects.all().delete()
        response = self.client.get("/api/city-count/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_get_city_count_not_found(self):
        response = self.client.get("/api/non-existent-endpoint/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetCitiesTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("weather_app.services.get_list_cities")
    def test_get_cities(self, mock_get_list_cities):
        mock_get_list_cities.return_value = ["Moscow", "Saint Petersburg"]
        response = self.client.get("/get-city/", {"q": "Mosk"})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            [
                "Москва",
                "Musk",
                "Middleton",
                "Моска",
                "Mosko",
                "Mosko",
                "Moské",
                "Моски",
                "al-Muski",
                "Moski",
            ],
        )

    @patch("weather_app.services.get_list_cities")
    def test_get_cities_no_query(self, mock_get_list_cities):
        response = self.client.get("/get-city/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [])

    @patch("weather_app.services.get_list_cities")
    def test_get_cities_query_too_short(self, mock_get_list_cities):
        mock_get_list_cities.return_value = []
        response = self.client.get("/get-city/", {"q": "Mo"})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [])
