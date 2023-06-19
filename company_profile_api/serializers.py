from rest_framework import serializers

from user_auth.serializers import UserInfoSerializer
from .models import *


class AboutUsSerializer(serializers.ModelSerializer):
    # user_info = UserInfoSerializer(source='user', read_only=True)

    class Meta:
        model = AboutUs
        fields = '__all__'
        read_only_fields = ('id',)


class SpecialTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialTeam
        fields = '__all__'
        read_only_fields = (
            'id',
        )


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'
        read_only_fields = ('id',)



class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'
        read_only_fields = ('id',)




class CompanyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyPolicy
        fields = '__all__'
        read_only_fields = (
            'id',
        )

