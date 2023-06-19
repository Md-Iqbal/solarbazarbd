import vendor
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.functions import Coalesce
# Create your views here.
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated
)

# from user_profile.serializers import (
#     CustomerProfileSerializer, RestaurantOwnerProfileSerializer
# )
from user_auth.permissions import IsAdmin, IsVendor
from .serializers import *


# Create your views here.



def get_product_category_list():
    return ProductCategory.objects.filter(is_active=True)


class DepartmentList(generics.ListCreateAPIView):
    """
    endpoint for creating product category for each vendor
    """
    permission_classes = (IsAdmin,)
    serializer_class = DepartmentSerializer
    queryset = Departments.objects.filter()

    def get_queryset(self):
        queryset = Departments.objects.all()
        return queryset

    def perform_create(self, serializer):
        if self.request.user.is_admin:
            try:
                serializer.save()
            except:
                raise ValidationError(
                    'Failed to add department')
        else:
            raise ValidationError(
                'You do not have access to create department')


class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    endpoint for retrieve update product category
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = DepartmentSerializer
    queryset = Departments.objects.all()


class ProductCategoryList(generics.ListCreateAPIView):
    """
    endpoint for creating product category for each vendor
    """
    permission_classes = ()
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.filter()

    def get_queryset(self):
        queryset = ProductCategory.objects.all()
        return queryset

    def perform_create(self, serializer):
        if self.request.user.is_admin:
            try:
                # department = get_object_or_404(Departments, pk=self.request.data['department_id'])
                serializer.save()
            except:
                raise ValidationError(
                    'Failed to add category')
        else:
            raise ValidationError(
                'You do not have access to create categories')




class ProductCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    endpoint for retrieve update product category
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()



class ProductSubCategoryList(generics.ListCreateAPIView):
    """
    endpoint for creating product category for each vendor
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSubCategorySerializer
    queryset = ProductSubCategory.objects.filter()

    def get_queryset(self):
        queryset = ProductSubCategory.objects.all()
        print(queryset)
        return queryset

    def perform_create(self, serializer):
        category = get_object_or_404(ProductCategory, pk=self.request.data['category_id'])
        print()
        # self.request.data.get('category'))
        serializer.save(category=category)
        # serializer.save()


class ProductSubCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    endpoint for retrieve update product category
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = ProductSubCategorySerializer
    queryset = ProductSubCategory.objects.filter()


class ProductMiniCategoryList(generics.ListCreateAPIView):
    """
    endpoint for creating product category for each vendor
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductMiniCategorySerializer
    queryset = ProductMiniCategory.objects.filter()

    def get_queryset(self):
        queryset = ProductMiniCategory.objects.all()
        print(queryset)
        return queryset

    def perform_create(self, serializer):
        subcategory = get_object_or_404(ProductSubCategory, pk=self.request.data['sub_category_id'])
        print(subcategory)
        # self.request.data.get('category'))
        serializer.save(sub_category=subcategory)
        # serializer.save()


class ProductMiniCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    endpoint for retrieve update product category
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = ProductMiniCategorySerializer
    queryset = ProductMiniCategory.objects.filter()


class ProductList(generics.ListAPIView):
    """
    endpoint for creating product category for each vendor
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)

    def get_queryset(self):
        category_filter = self.request.GET.get('category')
        print(category_filter)
        sort_order = self.request.GET.get('sort_order')
        if sort_order is None:
            sort_order='-created'
        if category_filter is None or category_filter == '-1':
            queryset = Product.objects.filter(is_active=True,).order_by(sort_order)
        else:
            queryset = Product.objects.filter(is_active=True,category_id = category_filter).order_by(sort_order)

        return queryset


class ProductCreate(generics.CreateAPIView):
    """
    endpoint for creating product category for each vendor
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        return queryset

    def perform_create(self, serializer):
        try:
            category = ProductCategory.objects.get(pk=self.request.data.get('category'))
        except:
            category = None
        try:
            sub_category = ProductSubCategory.objects.get(pk=self.request.data.get('sub_category'))
        except:
            sub_category = None
        try:
            vendor = Vendor.objects.get(id=self.request.user.id)
            serializer.save(category=category, sub_category=sub_category, vendor=vendor)
        except:
            raise ValidationError(
                'You do not have access to perform this action')


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    endpoint for retrieve update product category
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)


class ProductWarrantyList(generics.ListCreateAPIView):
    """
    endpoint for creating product category for each vendor
    """
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = WarrantySerializer
    def get_queryset(self):
        try:
            v_id = self.request.user.id
            queryset = ProductWarranty.objects.filter(vendor__id=v_id)
            return queryset
        except:
            raise ValidationError('You do not have access')
    # def get_queryset(self):
    #     queryset = ProductCategory.objects.all()
    #     return queryset
    #
    # def perform_create(self, serializer):
    #     serializer.save()

    def perform_create(self, serializer):
        try:
            vendor_ins = Vendor.objects.get(id=self.request.user.id)
            serializer.save(vendor=vendor_ins)
        except:
            raise ValidationError(
                'You do not have access to perform this action')


class ProductWarrantyUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    endpoint for retrieve update product category
    """
    permission_classes = (IsAuthenticated, IsAdmin,)
    serializer_class = WarrantySerializer
    queryset = ProductWarranty.objects.all()


class PromoCodeList(generics.ListCreateAPIView):
    """
    endpoint for viewing and creating promo code
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PromoCodeSerializer

    def get_queryset(self):
        user = self.request.user
        # if user.is_superuser:
        #     queryset = PromoCode.objects.all()
        # else:
        #     restaurant = SectionOwner().is_restaurant_owner(user)
        #     queryset = PromoCode.objects.filter(restaurant=restaurant)
        queryset = PromoCode.objects.filter(vendor__id=user.id)
        return queryset

    # def perform_create(self, serializer):
    #     user = self.request.user
    #     # restaurant = SectionOwner().is_restaurant_owner(user)
    #     # serializer.save(restaurant=restaurant)
    #     serializer.save()
    def perform_create(self, serializer):
        try:
            vendor_ins = Vendor.objects.get(id=self.request.user.id)
            serializer.save(vendor=vendor_ins)
        except:
            raise ValidationError(
                'You do not have access to perform this action')


class PromoCodeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    endpoint for retrieving updating and deleting promo code
    """
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = PromoCodeSerializer
    queryset = PromoCode.objects.all()


class PromoCodeData(generics.RetrieveAPIView):
    """
    endpoint for to get data of promo code
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PromoCodeSerializer
    queryset = PromoCode.objects.all()
    lookup_fields = ('code')

    def get_object(self):
        # user = self.request.user
        code = self.kwargs.get('code')
        # restaurant = self.kwargs.get('restaurant')
        # count_promocode_uses = FoodOrder.objects.filter(
        #     promo_code__code=code,
        #     customer__user__username=user
        # ).count()

        try:
            queryset = PromoCode.objects.get(code__iexact=code)
        except PromoCode.DoesNotExist:
            raise ValidationError('This is an invalid promo code')
        # if count_promocode_uses >= queryset.limit:
        #     raise ValidationError('Promo code limit exceeded')
        # elif queryset.is_valid:
        #     return queryset
        # raise ValidationError('code invalid')
        return queryset


class PurchaseListCreateView(generics.ListCreateAPIView):
    """
    endpoint for creating product category for each vendor
    """
    permission_classes = (IsAuthenticated, IsVendor)
    serializer_class = ProductPurchasedSerializer

    def get_queryset(self):
        queryset = ProductPurchased.objects.filter(vendor__user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        try:
            product = Product.objects.get(code=self.request.data.get('product_code'))
            supplier = Supplier.objects.get(id=self.request.data.get('supplier_id'))
            try:
                vendor_ins = Vendor.objects.get(id=self.request.user.id)
                serializer.save(vendor=vendor_ins, product=product, supplier=supplier)
                return serializer.data
            except Exception as e:
                print(e)
                raise ValidationError(
                    'You do not have access to perform this action')
        except Exception as e:
            print(e)
            raise ValidationError('Product not found')


class PurchaseDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    endpoint for retrieving updating and deleting promo code
    """

    permission_classes = (IsAuthenticated, IsVendor)
    serializer_class = ProductPurchasedSerializer

    def get_queryset(self):
        vendor = Vendor.objects.get(user = self.request.user)
        queryset = ProductPurchased.objects.filter(vendor=vendor)
        return queryset

# class FoodMenuDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsOwnerOrReadOnly,)
#     serializer_class = FoodMenuSerializer
#     queryset = FoodMenu.objects.all()
#     lookup_field = 'id'
#
#
# class MyFoodMenuList(generics.ListAPIView):
#     """
#     endpoint for logged restaurant owner food menus
#     """
#     permission_classes = (IsAuthenticated,)
#     serializer_class = FoodMenuSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         queryset = FoodMenu.objects.filter(restaurant__user=user)
#         return queryset
#
#
# class RestaurantFoodMenu(generics.ListAPIView):
#     """
#     endpoint for user to search food menu of a restaurant
#     by passing restaurant id
#     """
#     permission_classes = (IsAuthenticated,)
#     serializer_class = FoodMenuSerializer
#     queryset = FoodMenu.objects.all()
#
#     def get_queryset(self):
#         restaurant_id = self.request.query_params.get('restaurant_id',None)
#         queryset = FoodMenu.objects.filter(restaurant__id = restaurant_id,is_available=True)
#         return queryset


class GETProductDetail(generics.RetrieveAPIView):
    """
    endpoint for retrieving updating and deleting promo code
    """
    permission_classes = ()
    serializer_class = ProductSerializer
    lookup_field = 'code'
    queryset = Product.objects.all()


def search_all_product(request):
    titles = list()
    page_number = request.GET.get('page_no')
    if page_number == None or page_number == '':
        page_number = 1
    if 'term' in request.GET:
        # SearchVector search
        query_raw = (request.GET.get('term'))
        if query_raw =='' or query_raw is None:
            qs = Product.objects.all().order_by('-updated')
        else:
            search_string = prepare_search_term(query_raw)
            print(search_string)

            '''the best one so far'''
            qs = Product.objects.annotate(
                distance=((Coalesce(TrigramDistance(StringAgg('name', delimiter=' '), search_string, weight='D'), 1))
                          + Coalesce(TrigramDistance(StringAgg('code', delimiter=' '), search_string), 1)
                          + (Coalesce(TrigramDistance(StringAgg('alternative_names', delimiter=' '), search_string), 1) + 1)
                          ),
            ).filter(distance__lt=3.9).order_by('distance') #[:20]

        print(qs)

        '''---------Apply filter criteria-----------'''
        category_filter = request.GET.get('category')
        vendor_filter = request.GET.get('v')
        print(vendor_filter)
        sort_order = request.GET.get('sort_order')
        items_per_page = request.GET.get('items_per_page')
        if not (items_per_page is None or items_per_page == '-1' or items_per_page  == ''):
            items_per_page = 24
        if not (category_filter is None or category_filter == '-1'):
            qs = qs.filter(category_id=category_filter)

        if not (sort_order is None or sort_order == '-1'):
            qs = qs.all().order_by(sort_order)

        if not (vendor_filter is None or vendor_filter == '-1'):
            qs = Product.objects.filter(vendor__id=vendor_filter).order_by(sort_order)

        '''------------- pagination -------------'''
        paginator = Paginator(qs, items_per_page)  # number means items per page
        try:
            qs = paginator.page(int(page_number))
        except PageNotAnInteger:
            qs = paginator.page(1)
        except EmptyPage:
            qs = paginator.page(paginator.num_pages)

        titles = list()
        for product in qs:
            try:
                image = product.product_images.all()[0].image.thumbnail.url
            except:
                image = ''
            p = {
                'name': product.name,
                'code':  product.code,
                'price': product.discounted_price,
                'image':  image,
                'id':   product.id,
                'slug':   product.slug,
                'stock_quantity':   product.stock_quantity,
                'page_number': page_number,
                'number_of_pages': paginator.num_pages
            }
            titles.append(p)
        # titles = [product.title for product in qs]
    return JsonResponse(titles, safe=False)


def filter_categorized_product(request, slug):
    page_number = request.GET.get('page_no')
    sort_order = request.GET.get('sort_order')
    # min_price = decimal.Decimal(int(request.GET.get('min')))
    # max_price = decimal.Decimal(int(request.GET.get('max')))
    # print("minimum price: {min_price} and maximum price: {max_price}")
    if page_number == None or page_number == '':
        page_number = 1
    brand_filter = request.GET.get('brand')
    if slug == 'all':
        products = Product.objects.all()
        brand = Brand.objects.all()
    elif ProductCategory.objects.filter(slug=slug).exists():
        products = Product.objects.filter(category__slug=slug)
        cat = ProductCategory.objects.get(slug=slug)
        brand = Brand.objects.filter(type__icontains=cat.name)
        print('cat')

    elif ProductSubCategory.objects.filter(slug=slug).exists():
        products = Product.objects.filter(sub_category__slug=slug)
        sub_cat = ProductSubCategory.objects.get(slug=slug)
        brand = Brand.objects.filter(type__icontains=sub_cat.category.name)
        print('sub')
    elif ProductMiniCategory.objects.filter(slug=slug).exists():
        products = Product.objects.filter(mini_category__slug=slug)
        mini_cat = ProductMiniCategory.objects.get(slug=slug)
        brand = Brand.objects.filter(
            type__icontains=mini_cat.sub_category.category.name)
        print('mini')
    else:
        products = ''
        brand = None
    if not (sort_order is None or sort_order == '-1'):
        qs = products.all().order_by(sort_order)

    if brand_filter is not None:
        query = None
        or_query = None
        Brand_filter_list = brand_filter.split("_")
        print(Brand_filter_list)
        if Brand_filter_list == "-1":
            Brand_filter_list.clear()
        else:
            for B_id in Brand_filter_list:
                q = qs.filter(Q(brand__id=B_id))
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
            qs = query
            print(qs)

    '''------------- pagination -------------'''
    paginator = Paginator(
        qs, 20)  # items_per_page replaced by 20 # number means items per page
    try:
        qs = paginator.page(int(page_number))
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    titles = list()
    for product in qs:
        try:
            image = product.product_images.all()[0].image.thumbnail.url
        except:
            image = ''
        p = {
            'name': product.name,
            'code':  product.code,
            'image':  image,
            'id':   product.id,
            'slug':   product.slug,
            'stock_quantity':   product.stock_quantity,
            'discounted_price':   product.discounted_price,
            'price':   product.price,
            'page_number': page_number,
            'number_of_pages': paginator.num_pages
        }
        titles.append(p)
    return JsonResponse(titles, safe=False)


def VendorProduct(request, vendor_id):
    page_number = request.GET.get('page_no')
    sort_order = request.GET.get('sort_order')
    brand_filter = request.GET.get('brand')
    print(type(vendor_id))
    qs = Product.objects.filter(vendor__id=vendor_id)
    if page_number == None or page_number == '':
        page_number = 1

    print(qs)

    '''---------Apply filter criteria-----------'''
    items_per_page = request.GET.get('items_per_page')
    print(items_per_page)
    if not (items_per_page is None or items_per_page == '-1' or items_per_page == ''):
        items_per_page = 24

    if not (sort_order is None or sort_order == '-1'):
        qs = qs.all().order_by(sort_order)
    
    if brand_filter is not None:
        query = None
        or_query = None
        Brand_filter_list = brand_filter.split("_")
        print(Brand_filter_list)
        if Brand_filter_list == "-1":
            Brand_filter_list.clear()
        else:
            for B_id in Brand_filter_list:
                q = qs.filter(Q(brand__id=B_id))
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
            qs = query
    print(qs)

    '''------------- pagination -------------'''
    paginator = Paginator(qs, items_per_page)  # number means items per page
    try:
        qs = paginator.page(int(page_number))
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    titles = list()
    for product in qs:
        try:
            image = product.product_images.all()[0].image.thumbnail.url
        except:
            image = ''
        p = {
            'name': product.name,
            'code':  product.code,
            'image':  image,
            'id':   product.id,
            'slug':   product.slug,
            'stock_quantity':   product.stock_quantity,
            'discounted_price':   product.discounted_price,
            'price':   product.price,
            'page_number': page_number,
            'number_of_pages': paginator.num_pages
        }
        titles.append(p)
    return JsonResponse(titles, safe=False)


def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
   #return HttpResponse(url)
    if request.method == 'POST':  # check post
        print('form posted')
        form = CommentForm(request.POST)

        print(form)
        if form.is_valid():
            data = Comment()  # create relation with model
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.name = form.cleaned_data['name']
            data.rating = form.cleaned_data['rating']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id=id
            current_user= request.user
            data.user_id=current_user.id
            data.save()  # save data to table
            messages.success(request, "Your review has ben sent. Thank you for your interest.")
            return HttpResponseRedirect(url)
    messages.error(request, "Failed to submit your review. Make sure that you have submitted all the fields")

    return HttpResponseRedirect(url)
