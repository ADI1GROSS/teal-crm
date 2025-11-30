from rest_framework import serializers
from .models import Userprofile

class UserprofileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Userprofile
        fields = [
            "id",
            "invite_token",
            "fields",
            "name",
            "email",
            "phone",
            "regulations_document",
            "username",
            "user_email",
        ]
