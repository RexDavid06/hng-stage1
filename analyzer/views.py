from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.db import IntegrityError
from .models import AnalyzedString
from .serializers import CreateStringSerializer, AnalyzedStringSerializer
from .utils import analyse_string
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
import hashlib


# ------------------------------
# CREATE /strings (POST)
# ------------------------------
class CreateStringView(APIView):
    def post(self, request):
        serializer = CreateStringSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        value = serializer.validated_data.get("value")
        if not isinstance(value, str):
            return Response({"detail": "value must be a string"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        props = analyse_string(value)
        sha = props["sha256_hash"]

        if AnalyzedString.objects.filter(id=sha).exists():
            return Response({"detail": "String already exists"}, status=status.HTTP_409_CONFLICT)

        obj = AnalyzedString.objects.create(id=sha, value=value, properties=props)
        return Response(AnalyzedStringSerializer(obj).data, status=status.HTTP_201_CREATED)


# ------------------------------
# LIST /strings (GET)
# ------------------------------
class StringListView(ListAPIView):
    serializer_class = AnalyzedStringSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        qs = AnalyzedString.objects.all()
        params = self.request.query_params

        is_palindrome = params.get("is_palindrome")
        min_length = params.get("min_length")
        max_length = params.get("max_length")
        word_count = params.get("word_count")
        contains_character = params.get("contains_character")

        if is_palindrome:
            val = is_palindrome.lower() == "true"
            qs = [o for o in qs if o.properties.get("is_palindrome") == val]

        if min_length:
            qs = [o for o in qs if o.properties.get("length") >= int(min_length)]

        if max_length:
            qs = [o for o in qs if o.properties.get("length") <= int(max_length)]

        if word_count:
            qs = [o for o in qs if o.properties.get("word_count") == int(word_count)]

        if contains_character:
            if len(contains_character) != 1:
                raise ValueError("contains_character must be a single character")
            qs = [o for o in qs if contains_character in o.properties.get("character_frequency_map", {})]

        ids = [o.id for o in qs]
        from django.db.models import Case, When
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        return AnalyzedString.objects.filter(pk__in=ids).order_by("-created_at")


# DELETE /strings/{string_value}

class DeleteStringView(APIView):
    def delete(self, request, string_value):
        sha = hashlib.sha256(string_value.encode("utf-8")).hexdigest()

        try:
            obj = AnalyzedString.objects.get(pk=sha)
        except AnalyzedString.DoesNotExist:
            return Response(
                {"detail": "String does not exist in the system"},
                status=status.HTTP_404_NOT_FOUND
            )

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
