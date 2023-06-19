from rest_framework import serializers

from inventory_api.models import Brand
from inventory_api.models import Supplier
from .models import *

User = settings.AUTH_USER_MODEL


class PatchModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(PatchModelSerializer, self).__init__(*args, **kwargs)


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAgentProfile
        fields = '__all__'
        read_only_fields = ('id', 'user',)

