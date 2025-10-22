from rest_framework import serializers
from .models import AnalyzedString


class CreateStringSerializer(serializers.Serializer):
    value = serializers.CharField(required=True, allow_blank=False)

    def validate_value(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("value must be a string")
        return value


class AnalyzedStringSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyzedString
        fields = ["id", "value", "properties", "created_at"]
