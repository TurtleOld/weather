from django.http import JsonResponse
from django.core.cache import cache
from django.views.generic import FormView
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.views import APIView

from weather_app.forms import WeatherForm
from weather_app.models import CityCount
from weather_app.serializers import CityCountSerializer
from weather_app.services import get_weather_info, get_list_cities


class WeatherView(FormView):
    template_name = "weather.html"
    form_class = WeatherForm
    success_url = reverse_lazy("weather_app:weather")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()

        cached_weather = cache.get("last_weather")
        if cached_weather:
            context.update(cached_weather)
        
        cached_cities = cache.get("cached_cities", [])
        context["cached_cities"] = cached_cities

        return context

    def form_valid(self, form):
        city = form.cleaned_data.get("city")

        weather_info = get_weather_info(city)

        city_count, _ = CityCount.objects.get_or_create(city=city)
        city_count.count += 1
        city_count.save()
        
        cached_cities = cache.get("cached_cities", [])
        
        if city not in cached_cities:
            cached_cities.append(city)
            
        cache.set("cached_cities", cached_cities)

        context = self.get_context_data()
        context["weather_info"] = weather_info
        context["city"] = city

        cache.set("last_weather", {"weather_info": weather_info, "city": city})

        return self.render_to_response(context)


class CityCountAPIView(APIView):
    serializer_class = CityCountSerializer

    def get_queryset(self):
        return CityCount.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CityCountSerializer(queryset, many=True)
        return Response(serializer.data)


def get_cities(request) -> JsonResponse:
    query = request.GET.get("q", "")
    if len(query) > 3:
        cities = get_list_cities(query)
    else:
        cities = []
    return JsonResponse(cities, safe=False)
