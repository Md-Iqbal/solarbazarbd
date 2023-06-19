import datetime
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View
from rest_framework.permissions import OR

from customer_order_api.models import Order, PaymentDetails
from customer_profile_api.models import *
from inventory_api.models import *
from superadmin_api.models import StaticFiles
from user_auth.models import User
# Create your views here.
from user_auth.permissions import IsVendor, IsAdmin
from vendor_profile_api.models import Vendor


class VendorCheck(LoginRequiredMixin,UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_vendor



def user_login(request):
    url = request.GET.get("next", '')
    print('url' + url)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(User.objects.filter(username=username, password=password).values('username'))
        print(username)
        try:
            get_user = User.objects.get(username=username)
        except:
            get_user = None
        if get_user is not None:
            # user = User.objects.get(username=username, password=password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if url:
                    return HttpResponseRedirect(url)
                else:
                    return redirect('/vendor/myaccount/')
            else:
                messages.error(request, 'Password is incorrect')
                return render(request, 'vendor/auth-login.html', {'url': url})

        else:
            messages.error(request, 'User not found!')
            return render(request, 'vendor/auth-login.html', {'url': url})

    else:
        return render(request, 'vendor/auth-login.html', {'url': url})


def user_logout(request):
    logout(request)
    return redirect('user_login')


def myaccount(request):
    if request.user.is_vendor:
        url = '/vendor/'
    elif request.user.is_admin:
        url = '/superadmin/'
    else:
        url = '/'
    return redirect(url)


class MasterTemplateView(VendorCheck, TemplateView):
    template_name = 'vendor/master.html'


class IndexTemplateView(VendorCheck, TemplateView):
    template_name = 'vendor/index.html'


class ECommerceCartTemplateView(VendorCheck, TemplateView):
    template_name = 'vendor/ecommerce-cart.html'


class ECommerceCheckoutTemplateView(VendorCheck, TemplateView):
    template_name = 'vendor/ecommerce-checkout.html'


class ECommerceCustomerTemplateView(VendorCheck, TemplateView):
    template_name = 'vendor/ecommerce-customers.html'


class ECommerceDashboardTemplateView(VendorCheck, View):
    def get(self, request):
        today = datetime.date.today()
        vendor_id=self.request.user.id
        total_product = Product.objects.filter(vendor__id=vendor_id).count()
        total_order = Order.objects.filter(vendor__id=vendor_id).count()
        total_transaction = PaymentDetails.objects.filter(transaction_id='transaction_id').count()
        #sob payment details anle to onno vendor er transaction amount o cole ashbe abar payment details a vendor er foreign key nai
        total_revenue = PaymentDetails.objects.all().aggregate(Sum('amount_paid'))
        #problem
        today_sales = Order.objects.filter(vendor__id=vendor_id, created__year=today.year,
                                           created__month=today.month, created__day=today.day).aggregate(sum=Sum('order_total'))
        some_day_last_week = timezone.now().date() - datetime.timedelta(days=7)
        sunday_of_last_week = some_day_last_week - datetime.timedelta(days=(some_day_last_week.isocalendar()[2] - 0))
        sunday_of_this_week = sunday_of_last_week + datetime.timedelta(days=7)
        lastMonth_sales = Order.objects.filter(
            vendor__id=vendor_id, is_payment_successful=True, created__month=(today.month-1)).aggregate(sum=Sum('order_total'))
        lastWeek_sales = Order.objects.filter(
            vendor__id=vendor_id, is_payment_successful=True, created__gte=sunday_of_last_week, created__lt=sunday_of_this_week).aggregate(sum=Sum('order_total'))
        thisWeek_sales = Order.objects.filter(
            vendor__id=vendor_id, is_payment_successful=True, created__gte=sunday_of_this_week, created__lt=timezone.now().date()).aggregate(sum=Sum('order_total'))
        # top_transaction = Order.objects.filter(vendor__id=vendor_id,is_payment_successful=True).order_by('-order_total').values_list('order_total', flat=True).distinct()
        top_customers = Order.objects.filter(vendor__id=vendor_id).order_by('-order_total')[:5]

        recent_products = Product.objects.filter(vendor__id=vendor_id).order_by('-updated')[:5]
        print(recent_products)


        context = {
            'total_product': total_product,
            'total_order': total_order,
            'total_transaction': total_transaction,
            'total_revenue': total_revenue,
            'today_sales': today_sales,
            'lastMonth_sales': lastMonth_sales,
            'lastWeek_sales': lastWeek_sales,
            'thisWeek_sales': thisWeek_sales,
            'top_customers':top_customers,
            'recent_products':recent_products,
        }

        return render(request, 'vendor/ecommerce-dashboard.html', context)


class ECommerceOrderDetailsTemplateView(VendorCheck, TemplateView):
    def get(self, *args, **kwargs):
        id = kwargs['id']
        print(id)

        order = Order.objects.get(id=id)
        context = {
            'order': order,
        }
        print(order)
        return render(self.request, 'vendor/ecommerce-order-detail.html', context)

    def post(self, *args, **kwargs):
        id = kwargs['id']
        p_status = self.request.POST.get('p_status'),
        o_status = self.request.POST.get('o_status'),
        p_status = re.sub('[^a-zA-Z0-9 \n\.]', '', str(p_status))
        o_status = re.sub('[^a-zA-Z0-9 \n\.]', '', str(o_status))
        print(p_status)
        print(o_status)
        if o_status == 'PENDING':
            Order.objects.filter(id=id).update(status=o_status)
        elif o_status == 'ACCEPTED':
            Order.objects.filter(id=id).update(status=o_status, accepted_date=datetime.datetime.now())
        elif o_status == 'SHIPPING':
            Order.objects.filter(id=id).update(status=o_status, shipping_start_date=datetime.datetime.now())
        elif o_status == 'DONE' or o_status == 'CANCELED':
            Order.objects.filter(id=id).update(status=o_status, completed_date=datetime.datetime.now())
        order = Order.objects.get(id=id)
        PaymentDetails.objects.filter(order_payment=order).update(payment_status=p_status)

        return redirect('/vendor/order-details/' + str(id) + '/')


class ECommerceOrderTemplateView(VendorCheck, TemplateView):
    def get(self, *args, **kwargs):
        orders = Order.objects.filter(vendor__id=self.request.user.id)
        status = kwargs['status']
        print(status)
        if status == None or status == 'all':
            orders = orders.all().order_by('-created')
        else:
            orders = orders.filter(status=status).order_by('-created')
        context = {
            'orders': orders,
            'current_status': status,
        }
        print(orders)

        return render(self.request, 'vendor/ecommerce-orders.html', context)


class ECommerceProductDetailsTemplateView(VendorCheck, TemplateView):
    template_name = 'vendor/ecommerce-product-detail.html'


class ECommerceProductEditTemplateView(VendorCheck, View):
    def get(self, request):
        product_category = ProductCategory.objects.all()
        warranties = ProductWarranty.objects.all()
        brand = Brand.objects.all()
        vendor = Vendor.objects.all().values('id', 'company_name')
        context = {
            'vendor': vendor,
            'categories': product_category,
            'warranties': warranties,
            'brands': brand
        }
        return render(request, 'vendor/ecommerce-product-edit.html', context)


class ECommerceProductTemplateView(VendorCheck, TemplateView):
    def get(self, request):
        product_category = ProductCategory.objects.all()
        vendor_id = self.request.user.id
        context = {
            'categories': product_category,
            'vendor_id': vendor_id,
        }
        return render(request, 'vendor/ecommerce-products.html', context)


class ECommerceSellersTemplateView(VendorCheck, TemplateView):
    template_name = 'vendor/ecommerce-sellers.html'


class ECommerceAddCategoryView(VendorCheck, View):
    def get(self, request):
        product_category = ProductCategory.objects.all()
        vendor = Vendor.objects.all().values('id', 'company_name')
        brand= Brand.objects.all()
        context = {
            'vendor': vendor,
            'brands': brand,
            'product_category': product_category
        }
        return render(request, 'vendor/add-category.html', context)


class ECommerceAddSubCategoryView(VendorCheck, View):
    def get(self, request):
        product_category = ProductCategory.objects.filter(is_active=True)
        context = {
            'product_category': product_category
        }
        return render(request, 'vendor/add-sub-category.html', context)


class ECommercePorductCategoryView(VendorCheck, TemplateView):
    template_name = 'vendor/product-category.html'


class ECommerceProductSubCategoryView(VendorCheck, View):
    def get(self, request):
        product_category = ProductCategory.objects.all()
        context = {
            'product_category': product_category
        }
        return render(request, 'vendor/product-sub-category.html', context)


class ECommerceWarrantyView(VendorCheck, TemplateView):
    template_name = 'vendor/add-warranty.html'


class ECommerceAllWarrantyView(VendorCheck, TemplateView):
    template_name = 'vendor/warranty.html'


class ECommerceAddCouponView(VendorCheck, TemplateView):
    template_name = 'vendor/add-coupon.html'


class ECommerceAddDiscountView(VendorCheck, TemplateView):
    template_name = 'vendor/add-discount.html'


class ECommerceAllDiscountView(VendorCheck, TemplateView):
    template_name = 'vendor/product-discount.html'


class ECommerceAllCouponView(VendorCheck, TemplateView):
    template_name = 'vendor/product-coupon.html'


class AddProductPurchasedView(VendorCheck, TemplateView):
    def get(self, *args, **kwargs):
        suppliers = Supplier.objects.all()
        context = {
            'suppliers': suppliers
        }
        return render(self.request, 'vendor/add-product-purchased.html', context)


class ProductPurchasedView(VendorCheck, TemplateView):
    template_name = 'vendor/product-purchased.html'


class AddSupplierView(VendorCheck, TemplateView):
    template_name = 'vendor/add-supplier.html'

class InvoiceView(VendorCheck, TemplateView):
    def get(self, *args, **kwargs):
        id = kwargs['id']
        print(id)

        order = Order.objects.get(id=id)
        context = {
            'order': order,
            'static_files': StaticFiles.objects.filter(title='logo-img'),
        }

        return render(self.request, 'vendor/invoice.html', context)


class ManageSupplierView(VendorCheck, TemplateView):
    template_name = 'vendor/manage-suppliers.html'


class LoginPage(TemplateView):
    template_name = 'vendor/auth-login.html'


class MonthlyReportView(VendorCheck, View):
    def get(self, request):
        today = datetime.date.today()
        monthly_order = Order.objects.filter(created__month=today.month)
        method_amount = PaymentDetails.objects.values('payment_method').order_by('payment_method').annotate(
            amount=Sum('amount_paid'))

        today_sales = Order.objects.filter(vendor__user=self.request.user, created__year=today.year,
                                           created__month=today.month, created__day=today.day).aggregate(
            sum=Sum('order_total'))
        print(today_sales)

        context = {
            'monthly_order': monthly_order,
            'method_amount': method_amount,
            'today_sales': today_sales,
        }

        return render(request, 'vendor/monthly-report.html', context)


class DailyReportView(VendorCheck, TemplateView):
    template_name = 'vendor/daily-report.html'


class WeeklyReportView(VendorCheck, TemplateView):
    template_name = 'vendor/weekly-report.html'


class AddProduct(VendorCheck, View):
    def post(self, request, **kwargs):
        try:
            try:
                vendor_ins = Vendor.objects.get(user_id=self.request.user.id)
            except:
                print('You do not have access')
                messages.error(request, 'You do not have access to add products')
                return redirect('/vendor/e-commerce-product-edit/')
            discounted_price = float(self.request.POST.get('discounted_price'))
            price = float(self.request.POST.get('price'))
            if discounted_price >= price or discounted_price is None or discounted_price == 0.00 or discounted_price == 0:
                discounted_price = price
            product = Product.objects.create(
                vendor=vendor_ins,
                code=self.request.POST.get('code'),
                name=self.request.POST.get('name'),
                price=price,
                discounted_price=discounted_price,
                stock_quantity=self.request.POST.get('stock_quantity'),
                sub_category_id=self.request.POST.get('sub_category'),
                mini_category_id=self.request.POST.get('mini_category'),
                category=self.request.POST.get('category'),
                alternative_names=self.request.POST.get('alternative_names'),
                description=self.request.POST.get('description'),
                is_active=self.request.POST.get('is_active'),
                warranty_id_id=self.request.POST.get('warranty_id'),
                brand_id=self.request.POST.get('brand'),
                tax=self.request.POST.get('tax'),
                minimum_order_quantity=self.request.POST.get('minimum_order_quantity'),
                maximum_order_quantity=self.request.POST.get('maximum_order_quantity'),
                additional_info=self.request.POST.get('additional_info'),
            )
            product.save()
            print('success')

            try:
                image1 = self.request.FILES["image1"]
                img = ProductImages.objects.create(product=product, image=image1)
                img.save()
            except:
                print('image1 failed')
            try:
                image2 = self.request.FILES["image2"]
                img = ProductImages.objects.create(product=product, image=image2)
                img.save()
            except:
                print('image2 failed')
            try:
                image3 = self.request.FILES["image3"]
                img = ProductImages.objects.create(product=product, image=image3)
                img.save()
            except:
                print('image3 failed')

            try:
                image4 = self.request.FILES["image4"]
                img = ProductImages.objects.create(product=product, image=image4)
                img.save()
            except:
                print('image4 failed')
            # except:
            #     print('image failed')
            #     return redirect('/vendor/e-commerce-product-edit/')
        except Exception as e:
            print(e)
            messages.error(request, 'Failed to add product. Error = ' + str(e))
            return redirect('/vendor/e-commerce-product-edit/')
        messages.success(request, 'Product added successfully!')
        return redirect('/vendor/e-commerce-product-edit/')
        #
        # image1 = self.request.POST.get('image1')
        # image2 = self.request.POST.get('image2')
        # image3 = self.request.POST.get('image3')
        # image4 = self.request.POST.get('image4')
        #
        # print(code)
        # print(name)
        # print(price)
        # print(stock_quantity)
        # print(is_active)
        # print(warranty_id)


class ProductEditView(VendorCheck, View):
    def get(self, *args, **kwargs):
        product = Product.objects.get(slug=kwargs['slug'])
        product_category = ProductCategory.objects.filter(is_active=True)
        images = ProductImages.objects.filter(product=product)
        brand = Brand.objects.all()
        context = {
            'categories': product_category,
            'product': product,
            'images': images,
            'brands': brand,
        }
        return render(self.request, 'vendor/ecommerce-product-update.html', context)

    def post(self, request, **kwargs):
        print(self.request.POST.get('sub_category'))
        try:
            try:
                vendor_ins = Vendor.objects.get(user_id=self.request.user.id)
            except:
                print('You do not have access')
                messages.error(request, 'You do not have access to add products')
                return redirect('/vendor/product-details/' + kwargs['slug'] + '/')
            discounted_price = float(self.request.POST.get('discounted_price'))
            price = float(self.request.POST.get('price'))
            if discounted_price >= price or discounted_price is None or discounted_price == 0.00 or discounted_price == 0:
                discounted_price = price
            brand =self.request.POST.get('brand')
            if not brand.isnumeric():
                brand=None
            product = Product.objects.get(slug=kwargs['slug'])
            product.code = self.request.POST.get('code')
            product.name = self.request.POST.get('name')
            product.price = price
            product.discounted_price = discounted_price
            product.stock_quantity = self.request.POST.get('stock_quantity')
            product.sub_category_id = self.request.POST.get('sub_category')
            product.mini_category_id = self.request.POST.get('mini_category')
            product.category_id = ProductSubCategory.objects.get(id=self.request.POST.get('sub_category')).category_id
            product.alternative_names = self.request.POST.get('alternative_names')
            product.description = self.request.POST.get('description')
            product.is_active = self.request.POST.get('is_active')
            product.warranty_id_id = self.request.POST.get('warranty_id')
            product.brand_id = brand
            product.tax = self.request.POST.get('tax')
            product.minimum_order_quantity = self.request.POST.get('minimum_order_quantity')
            product.maximum_order_quantity = self.request.POST.get('maximum_order_quantity')
            product.additional_info = self.request.POST.get('additional_info')
            product.save()
            print('success')

            try:
                image1 = self.request.FILES["image1"]
                if image1:
                    ProductImages.objects.filter(id=self.request.POST.get('img1')).delete()
                    img = ProductImages.objects.create(product=product, image=image1)
                    img.save()
            except:
                print('image1 failed')
            try:
                image2 = self.request.FILES["image2"]
                if image2:
                    try:
                        ProductImages.objects.filter(id=self.request.POST.get('img2', -1)).delete()
                    except:
                        print('Failed to delete image 2')
                    img = ProductImages.objects.create(product=product, image=image2)
                    img.save()
            except Exception as e:
                print('image2 failed. Error = '+str(e))
            try:
                image3 = self.request.FILES["image3"]
                if image3:
                    ProductImages.objects.filter(id=self.request.POST.get('img3')).delete()
                    img = ProductImages.objects.create(product=product, image=image3)
                    img.save()
            except:
                print('image3 failed')

            try:
                image4 = self.request.FILES["image4"]
                if image4:
                    ProductImages.objects.filter(id=self.request.POST.get('img3')).delete()
                    img = ProductImages.objects.create(product=product, image=image4)
                    img.save()
            except:
                print('image4 failed')
        except Exception as e:
            print(e)
            messages.error(request, 'Failed to update product')
            messages.error(request, e)
            return HttpResponseRedirect(request.path_info)

        messages.success(request, 'Product updated successfully!')
        return redirect('/vendor/products/')

        #
        # image1 = self.request.POST.get('image1')
        # image2 = self.request.POST.get('image2')
        # image3 = self.request.POST.get('image3')
        # image4 = self.request.POST.get('image4')
        #
        # print(code)
        # print(name)
        # print(price)
        # print(stock_quantity)
        # print(is_active)
        # print(warranty_id)

class VendorInfoUpdateView(VendorCheck, View):
    def get(self, *args, **kwargs):
        vendor_info = Vendor.objects.get(id=self.request.user.id)
        print(vendor_info)
        context = {
            'vendor_info': vendor_info,
        }
        return render(self.request, 'vendor/vendor-update.html', context)

    def post(self, request, **kwargs):
        # print(self.request.POST.get('sub_category'))
        try:
            try:
                vendor_update = Vendor.objects.get(id=self.request.user.id)
            except:
                print('You do not have access')
                messages.error(request, 'You do not have access to edit info')
                return redirect('/vendor/update/')
            vendor_update.name = self.request.POST.get('name')
            vendor_update.company_name = self.request.POST.get('company_name')
            vendor_update.company_owner_name = self.request.POST.get('company_owner_name')
            vendor_update.year_of_establishment = self.request.POST.get('year_of_establishment')
            vendor_update.type_of_business = self.request.POST.get('type_of_business')
            vendor_update.contact_person = self.request.POST.get('contact_person')
            vendor_update.mobile = self.request.POST.get('mobile')
            vendor_update.telephone = self.request.POST.get('telephone')
            vendor_update.address = self.request.POST.get('address')
            vendor_update.bank_name = self.request.POST.get('bank_name')
            vendor_update.account_number = self.request.POST.get('account_number')
            vendor_update.account_name = self.request.POST.get('account_name')
            vendor_update.account_holder_name = self.request.POST.get('account_holder_name')
            vendor_update.branch_name = self.request.POST.get('branch_name')
            vendor_update.type_of_account = self.request.POST.get('type_of_account')
            vendor_update.branch_address = self.request.POST.get('branch_address')
            vendor_update.routing_no = self.request.POST.get('routing_no')

            vendor_update.save()
            print('success')
# banner_image  optional_banner_image  profile_image
            # try:
            #     image1 = self.request.FILES["banner_image"]
            #     if image1:
            #         if vendor_update.banner_image:
            #             vendor_update.banner_image.delete()
            #         vendor_update.banner_image.create(banner_image=image1)
            # except:
            #     print('banner_image failed')
            # try:
            #     image2 = self.request.FILES["optional_banner_image"]
            #     if image2:
            #         if vendor_update.optional_banner_image:
            #             vendor_update.optional_banner_image.delete()
            #         vendor_update.optional_banner_image.create(optional_banner_image=image2)
            # except:
            #     print('optional_banner_image failed')
            # try:
            #     image3 = self.request.FILES["profile_image"]
            #     if image3:
            #         if vendor_update.profile_image:
            #             vendor_update.profile_image.delete()
            #         vendor_update.profile_image.create(profile_image=image3)
            # except:
            #     print('profile_image failed')

        except Exception as e:
            print(e)
            messages.error(request, 'Failed to update vendor')
            messages.error(request, e)
            return HttpResponseRedirect(request.path_info)

        messages.success(request, 'Profile updated successfully!')
        return redirect('/vendor/update/')


class CustomOrderView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'vendor/custom-order.html')


class AddCategoryView(TemplateView):
    template_name = 'vendor/add-category.html'


class CategoryView(TemplateView):
    template_name = 'vendor/product-category.html'


class AddSubCategoryView(View):
    def get(self, request):
        product_category = ProductCategory.objects.all()
        context = {
            'product_category': product_category
        }
        return render(request, 'vendor/add-sub-category.html', context)


class SubCategoryView(View):
    def get(self, request):
        product_category = ProductCategory.objects.all()
        context = {
            'product_category': product_category
        }
        return render(request, 'vendor/product-sub-category.html', context)


from django.contrib.postgres.search import TrigramDistance


def search_customer(request):
    if 'term' in request.GET:
        # SearchVector search
        query_raw = (request.GET.get('term'))
        search_string = prepare_search_term(query_raw)
        print(search_string)
        '''the best one so far'''
        qs = CustomerProfile.objects.annotate(
            distance=((Coalesce(TrigramDistance(StringAgg('phone', delimiter=' '), search_string, weight='D'), 1))
            ),
        ).filter(distance__lt=.9).order_by('distance')[:5]

        customer_info = list()
        for customer in qs:
            print(customer.distance)
            p = {
                'label': customer.phone,
                'name': customer.name,
                'add': customer.short_address,
            }
            customer_info.append(p)
        # titles = [product.title for product in qs]
        return JsonResponse(customer_info, safe=False)
    return render(request, 'vendor/custom-order.html')


def autocomplete(request):
    if 'term' in request.GET:
        # SearchVector search

        query_raw = (request.GET.get('term'))
        search_string = prepare_search_term(query_raw)
        print(search_string)

        '''used before adding search_vector_field in product model'''
        # vector = SearchVector(
        #         StringAgg('name', delimiter=' '),
        #         weight='A',
        #         config='english',
        #     )#+SearchVector('code', weight='B')

        '''can be used, but trigramDistance gives more performance'''
        # query = SearchQuery(search_string, search_type='raw')
        # qs = Product.objects.annotate(
        #     document=F('search_vector'),
        #     rank=SearchRank(
        #         F('search_vector'),
        #         query,
        #         normalization=2
        #     ),
        #
        # ).order_by('-rank','name')[:15]

        '''the best one so far'''
        qs = Product.objects.annotate(
            distance=((Coalesce(TrigramDistance(StringAgg('name', delimiter=' '), search_string, weight='D'), 1))
                      + Coalesce(TrigramDistance(StringAgg('code', delimiter=' '), search_string), 1)
                      + (Coalesce(TrigramDistance(StringAgg('alternative_names', delimiter=' '), search_string), 1) + 1)
                      ),
        ).filter(distance__lt=4).order_by('distance')[:20]

        # TrigramSimilarity search
        # qs = Product.objects.annotate(
        #     similarity=TrigramSimilarity('name', request.GET.get('term')),
        # ).filter(similarity__gt=0.3).order_by('-similarity')
        # qs = Product.objects.filter(body_text__search=request.GET.get('term'))

        '''in depth search using custom modelManager'''
        # qs = Product.objects.search(query_raw)
        print(qs)
        # qs = Product.objects.annotate(
        #     search=SearchVector('name') + SearchVector('category__name'),
        #     rank=SearchRank(
        #         vector,
        #         query,
        #     ),
        # ).filter(search=request.GET.get('term')).order_by('-rank')

        titles = list()
        for product in qs:
            print(product.distance)
            try:
                image = product.product_images.all()[0].image.thumbnail.url
            except:
                image = ''
            p = {
                'label': product.name,
                'url': product.id,
                'code': product.code,
                'price': product.discounted_price,
                'image': image,
                'pid': product.id,
            }
            titles.append(p)
        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)
    return render(request, 'vendor/custom-order.html')


def test(request):
    return render(request, '1234.html')


class QSearch(View):
    import re
    def normalize_query(self, query_string,
                        findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                        normspace=re.compile(r'\s{2,}').sub):
        ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
            and grouping quoted words together.
            Example:
            ''''''>>> normalize_query('  some random  words "with   quotes  " and   spaces')
            ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
        '''
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

    def get_query(self, query_string, search_fields):
        ''' Returns a query, that is a combination of Q objects. That combination
            aims to search keywords within a model by testing the given search fields.

        '''
        query = None  # Query to search for every search term
        terms = self.normalize_query(query_string)
        for term in terms:
            or_query = None  # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return query

    def get(self, request):
        query_string = ''
        found_entries = None
        if ('term' in request.GET) and request.GET['term'].strip():
            query_string = request.GET.get('term')

            entry_query = QSearch.get_query(self, query_string, ['name', 'code', 'sub_category__name'])

            found_entries = Product.objects.filter(entry_query)
            titles = list()
            for product in found_entries:
                titles.append(product.name)
                # titles = [product.title for product in qs]
            return JsonResponse(titles, safe=False)
        return render(request, 'vendor/custom-order.html')


# final search engine
def search_product(request):
    import json
    from django.http import Http404, HttpResponse

    search_term = request.GET.get('term', None)
    if not search_term:
        raise Http404('Send a search term')

    products = Product.objects.search(search_term)

    response_data = [
        {
            'rank': p.rank,
            'name': p.name,

        } for p in products
    ]
    for p in products:
        print(p.name)

    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json',
    )


def update_vendor_temp(request):
    user = User.objects.get(username='admin@fortunes')
    vendor = Vendor.objects.get(user = user)
    Product.objects.filter().update(vendor=vendor)
    ProductWarranty.objects.filter().update(vendor=vendor)
    Supplier.objects.filter().update(vendor=vendor)
    ProductPurchased.objects.filter().update(vendor=vendor)
    PromoCode.objects.filter().update(vendor=vendor)
    Brand.objects.filter().update(vendor=vendor)
    return redirect('/vendor/')
