from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Lead, Contact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "first_name",
            "second_name",
            "phone",
            "email",
            "role",
            "concat_address",
        ]


class LeadSerializer(serializers.ModelSerializer):

    contacts = ContactSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Lead
        fields = [
            "id",
            "bride_side",
            "groom_side",
            "address",
            "day",
            "hebrew_day",
            "hebrew_month",
            "hebrew_year",
            "date_gregorian",
            "hour",
            "hall",
            "additional_details",
            "additional_crew",
            "has_additional_crew",
            "video",
            "assistent",
            "status",
            "payment_status",
            "payment_method",
            "custom_fields",
            "created_by",
            "contacts",
        ]
