from rest_framework import serializers
from .models import Error


class ErrorSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            "id",
            "err_code",
            "err_string",
            "created_at",
        )
        model = Error
