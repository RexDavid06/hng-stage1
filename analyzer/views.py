from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.db import IntegrityError
from .models import AnalyzedString
from .serializers import CreateStringSerializer, AnalyzedStringSerializer
from .utils import analyse_string
import hashlib


# POST /strings/
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


# GET /strings
class StringListView(ListAPIView):
    serializer_class = AnalyzedStringSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = AnalyzedString.objects.all()
        params = self.request.query_params

        is_palindrome = params.get("is_palindrome")
        min_length = params.get("min_length")
        max_length = params.get("max_length")
        word_count = params.get("word_count")
        contains_character = params.get("contains_character")

        if is_palindrome is not None:
            val = is_palindrome.lower() == "true"
            queryset = queryset.filter(properties__is_palindrome=val)

        if min_length is not None:
            queryset = queryset.filter(properties__length__gte=int(min_length))

        if max_length is not None:
            queryset = queryset.filter(properties__length__lte=int(max_length))

        if word_count is not None:
            queryset = queryset.filter(properties__word_count=int(word_count))

        if contains_character:
            if len(contains_character) != 1:
                return AnalyzedString.objects.none()
            queryset = queryset.filter(
                **{f"properties__character_frequency_map__has_key": contains_character}
            )

        return queryset.order_by("-created_at")


# GET /strings/{string_value}
class RetrieveStringView(APIView):
    def get(self, request, string_value):
        sha = hashlib.sha256(string_value.encode("utf-8")).hexdigest()
        obj = AnalyzedString.objects.filter(id=sha).first()
        if not obj:
            return Response({"detail": "String not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(AnalyzedStringSerializer(obj).data, status=status.HTTP_200_OK)


# DELETE /strings/{string_value}
class DeleteStringView(APIView):
    def delete(self, request, string_value):
        sha = hashlib.sha256(string_value.encode("utf-8")).hexdigest()
        obj = AnalyzedString.objects.filter(id=sha).first()
        if not obj:
            return Response({"detail": "String does not exist in the system"}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# GET /strings/filter-by-natural-language
class NaturalLanguageFilterView(APIView):
    def get(self, request):
        query = request.query_params.get("query", "").lower()
        queryset = AnalyzedString.objects.all()

        if "palindrome" in query:
            if "not" in query:
                queryset = queryset.filter(properties__is_palindrome=False)
            else:
                queryset = queryset.filter(properties__is_palindrome=True)

        if "longer than" in query:
            import re
            match = re.search(r"longer than (\d+)", query)
            if match:
                length = int(match.group(1))
                queryset = queryset.filter(properties__length__gt=length)

        if "shorter than" in query:
            import re
            match = re.search(r"shorter than (\d+)", query)
            if match:
                length = int(match.group(1))
                queryset = queryset.filter(properties__length__lt=length)

        if "contain" in query:
            import re
            match = re.search(r"contain[s]? (.)", query)
            if match:
                char = match.group(1)
                queryset = queryset.filter(
                    **{f"properties__character_frequency_map__has_key": char}
                )

        return Response(AnalyzedStringSerializer(queryset, many=True).data, status=status.HTTP_200_OK)
