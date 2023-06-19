from django.conf import settings
from rest_framework import serializers
User = settings.AUTH_USER_MODEL


class UserInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name')

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'date_joined',
            'last_login',
            'is_active',
            'is_staff',
            'is_customer',
            'is_admin',
            'phone',
            'full_name',
        )
