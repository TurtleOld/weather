from django.urls import path

from weather_app.views import WeatherView, get_cities, CityCountAPIView

app_name = "weather_app"
urlpatterns = [
    path("", WeatherView.as_view(), name="weather"),
    path(
        "get-city/",
        get_cities,
        name="get_cities",
    ),
    path("api/city-count/", CityCountAPIView.as_view(), name="city_count_api"),
]
