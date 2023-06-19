from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from .models import *

User = settings.AUTH_USER_MODEL


class PatchModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(PatchModelSerializer, self).__init__(*args, **kwargs)


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ('id',)


class ProductSubCategorySerializer(serializers.ModelSerializer):
    # image = Base64ImageField()
    # category = serializers.PrimaryKeyRelatedField(read_only=True)
    # category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all())
    category = 'ProductCategorySerializer()'
    category_name = serializers.CharField(
        source="category.category_name",
        read_only=True
    )
    category_id = 'category_id'

    class Meta:
        model = ProductSubCategory
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated',
        )
        depth = 5


class ProductMiniCategorySerializer(serializers.ModelSerializer):
    # image = Base64ImageField()
    # category = serializers.PrimaryKeyRelatedField(read_only=True)
    # category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all())
    sub_category = 'ProductSubCategorySerializer()'
    sub_category_name = serializers.CharField(
        source="sub_category.name",
        read_only=True
    )

    class Meta:
        model = ProductMiniCategory
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated',
        )
        depth = 3


class ProductCategorySerializer(WritableNestedModelSerializer):
    product_subcategory_category = ProductSubCategorySerializer(many=True, read_only=True)
    department = serializers.PrimaryKeyRelatedField(queryset=Departments.objects.all())

    class Meta:
        model = ProductCategory
        fields = '__all__'

        read_only_fields = (
            'id',
            'created',
            'updated',

        )
        depth = 5

    # def update(self, instance, data):
    #     print('This is department id: ' + str(data.get('department')))
    #     try:
    #         department = Departments.objects.get(id=data.pop('department'))
    #     except:
    #         department = None
    #     instance.department = department
    #     instance.save()
    #     return instance


class DepartmentSerializer(WritableNestedModelSerializer):
    department_category = ProductCategorySerializer(many=True, read_only=True)
    category_name = serializers.CharField(
        source="category.category_name",
        read_only=True
    )

    class Meta:
        model = Departments
        fields = '__all__'
        read_only_fields = ('id',)
        depth = 3


class ProductImageSerializer(serializers.ModelSerializer):
    product_id = 'product_id'

    class Meta:
        model = ProductImages
        fields = '__all__'
        read_only_fields = (
            'id',
            'product',
        )


class ProductSerializer(WritableNestedModelSerializer):
    # image = Base64ImageField()
    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )
    category_id = 'category_id'
    sub_category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )
    sub_category_id = 'sub_category_id'
    product_images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated',
            'vendor',
        )
        depth = 5


class WarrantySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductWarranty
        fields = '__all__'
        read_only_fields = (
            'id',
            'slug',
            'vendor'
        )


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated',
            'vendor'
        )


class ProductPurchasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPurchased
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'updated',
            'product',
            'supplier',
            'slug',
            'vendor',
        )
