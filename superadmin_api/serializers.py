
from .models import *
from inventory_api.models import Brand
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


class StaticFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticFiles
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated'
        )


class MainSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainSlider
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated'
        )


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
        read_only_fields = ('id',)
