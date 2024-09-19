from rest_framework import serializers
from ..models import GenreItem


class GenreItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreItem
        fields = '__all__'
