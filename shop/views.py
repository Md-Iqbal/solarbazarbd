import datetime

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import CsrfExemptMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.functions import Coalesce
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View

from company_profile_api.models import *
from customer_order_api.models import Order, PaymentDetails
from customer_profile_api.models import *
from inventory_api.models import *
from superadmin_api.models import MainSlider
from superadmin_api.models import StaticFiles
from user_auth.models import User

# Create your views here.

def get_product_category_list():
    return ProductCategory.objects.filter(is_active=True)


class Blog(TemplateView):
    template_name = 'blog.html'


class BlogSingle(TemplateView):
    template_name = 'blog-single.html'


class Cart(View):
    def get(self, request):
        departments = Departments.objects.all()
        category = ProductCategory.objects.filter(is_active=True)
        context = {
            'categories': category,
            'departments': departments,
        }
        return render(request, 'mobile-cart.html', context)


class Checkout(View):
    def get(self, request):
        customer_details = CustomerProfile.objects.get(user=self.request.user)
        departments = Departments.objects.all()
        category = ProductCategory.objects.filter(is_active=True)
        print(customer_details.name)
        context = {
            'customer': customer_details,
            'categories': category,
            'departments': departments,
        }
        return render(request, 'checkout.html', context)


class Contact(View):
    def get(self, request):
        contact_info = ContactUs.objects.all()
        departments = Departments.objects.all()
        category = ProductCategory.objects.filter(is_active=True)
        context = {
            'contact_info': contact_info[0],
            'categories': category,
            'departments': departments,
        }
        return render(request, 'contact.html', context)


class Index(View):
    def get(self, request, *args, **kwargs):
        # from django.db import connection
        # with connection.cursor() as cursor:
        #     cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')

        departments = Departments.objects.all()
        category = ProductCategory.objects.filter(is_active=True)
        vendors = Vendor.objects.filter(status='Active')
        solar_panels = Product.objects.filter((Q(category__name__icontains='Panel') |
                                               Q(sub_category__name__icontains='Panel')), is_active=True)
        solar_street_light = Product.objects.filter((Q(category__name__icontains='Street Light') |
                                                     Q(sub_category__name__icontains='Street Light')),
                                                    is_active=True)
        solar_pam_system = Product.objects.filter((Q(category__name__icontains='Pump') |
                                                   Q(sub_category__name__icontains='Pump')),
                                                  is_active=True)
        # product = Product.objects.filter(is_active=True)
        static_files = StaticFiles.objects.all()
        main_slider = MainSlider.objects.all()

        context = {
            'categories': category,
            'solar_panels': solar_panels,
            'solar_street_light': solar_street_light,
            'solar_pam_system': solar_pam_system,
            'static_files': static_files,
            'main_slider': main_slider,
            'departments': departments,
            'vendors': vendors,
        }
        # print(len(category))
        return render(request, 'index.html', context)


class OrderReceived(TemplateView):
    template_name = 'order-received.html'


class ProductCategoryView(TemplateView):
    template_name = 'product-category.html'


class Shop(View):
    def get(self, request, *args, **kwargs):
        try:
            brand_filter = request.GET.get('brand')
        except:
            brand_filter = None

        slug = self.kwargs.get('slug')
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
        print(len(products))
        static_files = StaticFiles.objects.all()
        departments = Departments.objects.all()
        # Min_price = Product.objects.aggregate(Min('price'))['price__min']
        # Max_price = Product.objects.aggregate(Max('price'))['price__max']
        category = ProductCategory.objects.filter(is_active=True)
        # min_price_product = Product.objects.filter(price=Min_price).values('price')
        # print(min_price_product)
        if brand_filter:
            products = products.filter(brand__slug=brand_filter)

        context = {
            'categories': category,
            'departments': departments,
            'products': products,
            'static_files': static_files,
            'brands': brand,
            'cat_slug': slug,
            # 'Min_price': Min_price,
            # 'Max_price': Max_price,
            # 'min_price_product':min_price_product,
        }
        return render(request, 'single-category-product.html', context)

def VendorShop(request, vendor_id):
    products = Product.objects.filter(vendor__id=vendor_id)
    vendor_info = Vendor.objects.get(id = vendor_id)
    static_files = StaticFiles.objects.all()
    departments = Departments.objects.all()
    category = ProductCategory.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    context = {
        'categories': category,
        'departments': departments,
        'products': products,
        'static_files': static_files,
        'vendor_info': vendor_info,
        'vendor_id':vendor_id,
        'brands':brands,
        # 'vendor_images':vendor_images,
    }
    return render(request, 'single_vendor_product.html', context)

class ShopFullWidth(TemplateView):
    template_name = 'shop-fullwidth.html'


class SingleProductFullWidth(TemplateView):
    template_name = 'single-product-fullwidth.html'


class TrackYourOrder(TemplateView):
    template_name = 'track-your-order.html'


class Wishlist(View):
    def get(self, request):
        departments = Departments.objects.all()
        category = ProductCategory.objects.filter(is_active=True)
        context = {
            'categories': category,
            'departments': departments,
        }
        return render(request, 'wishlist.html', context)


class Error404(TemplateView):
    template_name = '404.html'


class VendorApplication(TemplateView):
    def get(self, request):
        departments = Departments.objects.all()
        category = ProductCategory.objects.filter(is_active=True)
        context = {
            'categories': category,
            'departments': departments,
        }
        return render(request, 'become-vendor.html', context)


def get_product_details(request):
    p_id = request.GET.get('p_id', None)
    p_details = Product.objects.get(pk=p_id)
    # data = sr.serialize('json', p_details)
    print(p_details)
    return HttpResponse(p_details)


def single_product_view(request, id):
    single_product = Product.objects.get(id=id)
    related_product = Product.objects.filter(category_id=single_product.category_id)
    reviews = Comment.objects.filter(product=single_product)
    star1 = 0
    star2 = 0
    star3 = 0
    star4 = 0
    star5 = 0
    try:
        ratingcount = Comment.objects.raw(
            'SELECT rating id, COUNT(id) count  from inventory_api_comment group by rating,product_id having product_id = ' + str(
                single_product.id))
        for c in ratingcount:
            if c.id == 1:
                star1 = c.count
            elif c.id == 2:
                star2 = c.count
            elif c.id == 3:
                star3 = c.count
            elif c.id == 4:
                star4 = c.count
            elif c.id == 5:
                star5 = c.count
    except Exception as e:
        print(e)

    departments = Departments.objects.all()
    context = {
        'single_product': single_product,
        'related_product': related_product,
        'categories': get_product_category_list,
        'departments': departments,
        'reviews': reviews,
        'star1': star1,
        'star2': star2,
        'star3': star3,
        'star4': star4,
        'star5': star5,
    }

    return render(request, 'single-product-fullwidth.html', context)


def about_us(request):
    about = AboutUs.objects.all()
    team = SpecialTeam.objects.all().order_by('priority')
    departments = Departments.objects.all()
    category = ProductCategory.objects.filter(is_active=True)
    context = {
        'about': about[0],
        'team': team,
        'categories': category,
        'departments': departments,
    }
    return render(request, 'about.html', context)


def faq_view(request):
    faq = Faq.objects.all()
    departments = Departments.objects.all()
    category = ProductCategory.objects.filter(is_active=True)
    context = {
        'faq': faq,
        'categories': category,
        'departments': departments,

    }
    return render(request, 'faq.html', context)


def company_policy(request):
    policy = CompanyPolicy.objects.filter(title__iexact='Privacy Policy')
    departments = Departments.objects.all()
    category = ProductCategory.objects.filter(is_active=True)
    context = {
        'policy': policy,
        'categories': category,
        'departments': departments,
    }
    return render(request, 'privacy-policy.html', context)


def terms_and_conditions(request):
    tc = CompanyPolicy.objects.filter(title__iexact='Terms and Conditions')
    departments = Departments.objects.all()
    category = ProductCategory.objects.filter(is_active=True)
    context = {
        'policy': tc,
        'categories': category,
        'departments': departments,
    }
    return render(request, 'terms-and-conditions.html', context)


def return_refunt_policy(request):
    tc = CompanyPolicy.objects.filter(title__iexact='Return and Refund Policy')
    departments = Departments.objects.all()
    category = ProductCategory.objects.filter(is_active=True)
    context = {
        'policy': tc,
        'categories': category,
        'departments': departments,
    }
    return render(request, 'return-refund-policy.html', context)


class ProductView(View):
    def get(self, request, slug):
        subcategory_wise_product = ProductSubCategory.objects.filter(category__slug=slug)
        departments = Departments.objects.all()
        category = ProductCategory.objects.filter(is_active=True)
        print(subcategory_wise_product)
        static_files = StaticFiles.objects.all()
        context = {
            'categories': category,
            'departments': departments,
            'static_files': static_files,
        }

        template_name = 'product.html'
        return render(request, template_name, context)


class DepartmentView(View):
    def get(self, request, slug):
        category_wise_product = ProductCategory.objects.filter(department__slug=slug)
        print(category_wise_product)
        static_files = StaticFiles.objects.all()
        departments = Departments.objects.all()
        category = ProductCategory.objects.filter(is_active=True)
        context = {
            'categories': category,
            'departments': departments,
            'category_wise_product': category_wise_product,
            'static_files': static_files,
        }

        template_name = 'product.html'
        return render(request, template_name, context)


class SingleProductCategoryView(TemplateView):
    template_name = 'single-category-product.html'


def login_required(request):
    return HttpResponse("<script>$('#loginModal').modal('show')</script>")


def customer_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        print(username)
        print(password)
        if User.objects.filter(username=username, password=password).exists():
            messages.error(request, 'Account already exists with this phone: ' + str(username))
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        else:
            try:
                user = User.objects.create(username=username,  is_customer=True, email=email)
                user.set_password(password)
                user.save()
                print(user)
                if user is not None:
                    print('user created')
                    # user = User.objects.get(username=username, password=password)
                    # user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        messages.success(request, 'Sign up successful: ' + str(username))
                        print('Yeah logged in!')
                        customer = CustomerProfile.objects.create(user=user, phone=username, email=email)
                        next = request.POST.get('next', '/')
                        return HttpResponseRedirect(next)
                    else:
                        print('user not authenticated')
                        messages.error(request, 'Password is incorrect')
                        next = request.POST.get('next', '/')
                        return HttpResponseRedirect(next)
            except Exception as e:
                print(e)
                messages.error(request, 'Failed to create account: ' + str(username))
                next = request.POST.get('next', '/')

    else:
        return render(request, 'customer-signup.html')


def customer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # print(User.objects.filter(username=username, password=password).values('username'))
        print(username)
        print(password)
        try:
            get_user = User.objects.get(username=username)
            print(get_user)
        except:
            get_user = None
        if get_user is not None:
            print('user found')
            # user = User.objects.get(username=username, password=password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful')
                print('Yeah logged in!')
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)
            else:
                print('user not authenticated')
                messages.error(request, 'Password is incorrect')
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)

        else:
            messages.error(request, 'User not found!')
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    else:
        return render(request, 'customer-login.html')


def customer_logout(request):
    logout(request)
    return redirect('/')


def OTP_VerificationView(request):
    return render(request, 'otp-verification.html')


class OrderDetailsTemplateView(LoginRequiredMixin, CsrfExemptMixin, View):
    def get(self, *args, **kwargs):
        id = kwargs['id']
        print(id)

        order = Order.objects.get(id=id, customer__user=self.request.user)
        context = {
            'order': order,
        }
        print(order)
        return render(self.request, 'order-detail.html', context)


class OrderInvoiceView(LoginRequiredMixin, TemplateView):
    def get(self, *args, **kwargs):
        id = kwargs['id']
        print(id)

        order = Order.objects.get(id=id, customer__user=self.request.user)
        context = {
            'order': order,
            'static_files': StaticFiles.objects.filter(title='logo-img'),
        }

        return render(self.request, 'invoice.html', context)


class MyOrdersView(LoginRequiredMixin, CsrfExemptMixin, View):
    def get(self, *args, **kwargs):
        orders = Order.objects.filter(customer__user=self.request.user).order_by('-created')

        context = {
            'orders': orders,
        }
        print(orders)

        return render(self.request, 'my-orders.html', context)


class MyAccountView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        customer = CustomerProfile.objects.get(user=self.request.user)
        # orders = Order.objects.raw('SELECT status as id, COALESCE(count(id),0) as scount FROM customer_order_api_order where customer_id = '+str(customer.id)+' GROUP BY status')

        all_orders = Order.objects.filter(customer=customer).count()
        pending_orders = Order.objects.filter(customer=customer, status='PENDING').count()
        done_orders = Order.objects.filter(customer=customer, status='DONE').count()

        context = {
            'customer': customer,
            'all_orders': all_orders,
            'pending_orders': pending_orders,
            'done_orders': done_orders,
        }

        return render(self.request, 'customer-account.html', context)

    def post(self, *args, **kwargs):
        try:
            if CustomerProfile.objects.filter(user=self.request.user).exists():
                customer = CustomerProfile.objects.filter(user=self.request.user).update(
                    name=self.request.POST.get('name'),
                    phone=self.request.POST.get('phone'),
                    email=self.request.POST.get('email'),
                    short_address=self.request.POST.get('short_address'),
                )
            else:
                customer = CustomerProfile.objects.create(
                    user=self.request.user,
                    name=self.request.POST.get('name'),
                    phone=self.request.POST.get('phone'),
                    email=self.request.POST.get('email'),
                    short_address=self.request.POST.get('short_address'),
                )
            customer = CustomerProfile.objects.get(user=self.request.user)
            if CustomerAddress.objects.filter(customer=customer).exists():
                CustomerAddress.objects.filter(customer=customer).update(
                    zip_code=self.request.POST.get('zip_code'),
                    area=self.request.POST.get('area'),
                    house_number=self.request.POST.get('house_number'),
                    flat_number=self.request.POST.get('flat_number'),
                    city=self.request.POST.get('city'),
                    street=self.request.POST.get('street'),
                )
            else:
                CustomerAddress.objects.create(
                    zip_code=self.request.POST.get('zip_code'),
                    area=self.request.POST.get('area'),
                    house_number=self.request.POST.get('house_number'),
                    flat_number=self.request.POST.get('flat_number'),
                    city=self.request.POST.get('city'),
                    street=self.request.POST.get('street'),
                    customer=customer
                )
            messages.success(self.request, 'Your profile has been updated!')
        except Exception as e:
            print(e)
            messages.error(self.request, 'Failed to update profile information')

        return redirect('/profile/')


def myaccount(request):
    if request.user.is_customer:
        pass


def search(request):
    term = request.GET.get('term')
    r = requests.get(
        'https://solarbazarbd.com/api/v1/inventory/search-all-product/?term=' + term + '&page_no=1&items_per_page=30',
        params=request.GET)
    print(r.json())
    return render(request, 'search.html')




def search_all_product(request):
    titles = list()
    page_number = 1 #request.GET.get('page_no')
    if page_number == None or page_number == '':
        page_number = 1
    if 'term' in request.GET:
        # SearchVector search
        query_raw = (request.GET.get('term'))
        if query_raw =='' or query_raw is None:
            qs = Product.objects.all().order_by('-updated')[:40]
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
        # sort_order = request.GET.get('sort_order')
        items_per_page = 30#request.GET.get('items_per_page')
        if not (items_per_page is None or items_per_page == '-1' or items_per_page  == ''):
            items_per_page = 20
        if not (category_filter is None or category_filter == 'all'):
            qs = qs.filter(category__slug=category_filter)

        # if not (sort_order is None or sort_order == '-1'):
        #     qs = qs.all().order_by(sort_order)

        '''------------- pagination -------------'''
        # paginator = Paginator(qs, items_per_page)  # number means items per page
        # try:
        #     qs = paginator.page(int(page_number))
        # except PageNotAnInteger:
        #     qs = paginator.page(1)
        # except EmptyPage:
        #     qs = paginator.page(paginator.num_pages)
        #
        # titles = list()

        # titles = [product.title for product in qs]
    else:
        qs = None
    return render(request,'search_result.html',{'products':qs})



class CreatePayment(View):
    def get(self, request, **kwargs):

        order_id = self.kwargs['order_id']
        order = Order.objects.get(id=order_id)

        dt = datetime.datetime.now()
        seq = int(dt.strftime("%Y%m%d%H%M%S"))

        email = order.customer.email
        if email:
            email = email
        else:
            email = 'a@b.com'

        trx = "TX"+str(order.id)+str(seq)

        from sslcommerz_lib import SSLCOMMERZ
        settings = {'store_id': 'fortu60ee90da6583a', 'store_pass': 'fortu60ee90da6583a@ssl', 'issandbox': True}
        sslcz = SSLCOMMERZ(settings)

        post_body = {}
        post_body['total_amount'] = order.order_total
        post_body['currency'] = "BDT"
        post_body['tran_id'] = trx
        post_body['success_url'] = "http://127.0.0.1:8000/success-payment/"+order_id+'/'+trx+'/'
        post_body['fail_url'] = "http://127.0.0.1:8000/order-details/"+order_id+'/'
        post_body['cancel_url'] = "http://127.0.0.1:8000/"
        post_body['emi_option'] = 0
        post_body['cus_name'] = order.customer.name
        post_body['cus_email'] = email
        post_body['cus_phone'] = order.customer.phone
        post_body['cus_add1'] = order.customer.short_address
        post_body['cus_city'] = order.delivery_address.city
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "No"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = order.item_count
        post_body['product_name'] = order.product_list
        post_body['product_category'] = "ecommerce"
        post_body['product_profile'] = "general"

        response = sslcz.createSession(post_body)  # API response
        print(response)
        return redirect(response['GatewayPageURL'])


class SuccessPayment(CsrfExemptMixin,View):
    def post(self, request, **kwargs):
        print("succes payment view function start")
        trx = self.kwargs['trx']
        order_id = self.kwargs['order_id']
        order = Order.objects.get(id=order_id)

        pay_ins = PaymentDetails.objects.create(
            payment_method='SSLCOMMERZ',
            payment_status='PAID',
            amount_paid=order.order_total,
            transaction_id=trx,
            is_failed=False
        )

        order.payment = pay_ins
        order.is_payment_successful = True
        order.save()
        print("succes payment view end")
        return redirect('/orders/')


class StoreLocationView(LoginRequiredMixin, CsrfExemptMixin, View):
    def get(self, *args, **kwargs):
        orders = Order.objects.filter(
            customer__user=self.request.user).order_by('-created')

        context = {
            'orders': orders,
        }
        print(orders)

        return render(self.request, 'my-orders.html', context)
