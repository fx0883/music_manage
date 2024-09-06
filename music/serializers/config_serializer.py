# your_app/serializers/config_serializer.py

from rest_framework import serializers
from ..models import Config


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ['id', 'name', 'value', 'created_at', 'updated_at']
