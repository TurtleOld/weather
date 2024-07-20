from rest_framework import serializers
from weather_app.models import CityCount


class CityCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = CityCount
        fields = ["city", "count"]
