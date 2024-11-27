from dataclasses import fields
import datetime

from django.forms import ValidationError
from models import Book, Author
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name"]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = "__all__"

    def validate(self, data):
        if datetime.date.year < data["publication_year"]:
            raise serializers.ValidationError("Date is in the future")
        return data
