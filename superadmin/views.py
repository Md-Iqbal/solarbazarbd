from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View

from business_agent.models import BusinessAgentProfile
from company_profile_api.models import *
from inventory_api.models import ProductCategory, Departments, ProductSubCategory, ProductImages, Product, Brand
from superadmin_api.models import StaticFiles
from vendor.views import VendorCheck
from vendor_profile_api.models import *


# Create your views here.


class SuperAdminIndexView(LoginRequiredMixin, View):
    def get(self, request):
        static_files = StaticFiles.objects.all()

        context = {
            'static_files': static_files
        }
        return render(request, 'superadmin/super-admin-dashboard.html', context)


class LogoUpload(LoginRequiredMixin, TemplateView):
    template_name = 'superadmin/upload-static.html'


class MainBannerUpload(LoginRequiredMixin, TemplateView):
    template_name = 'superadmin/upload-main-banner.html'


class PromotionalBannerUpload(LoginRequiredMixin, TemplateView):
    template_name = 'superadmin/upload-promotional-banner.html'


class Invoice(LoginRequiredMixin, TemplateView):
    template_name = 'superadmin/invoice.html'


class ViewMainSlider(LoginRequiredMixin, TemplateView):
    template_name = 'superadmin/view-main-slider.html'


class MemberList(LoginRequiredMixin, TemplateView):
    template_name = 'superadmin/member-list.html'


class AboutusView(LoginRequiredMixin, View):
    def get(self, request):
        aboutus_instance = AboutUs.objects.all()

        template_name = 'superadmin/aboutus.html'
        return render(self.request, template_name, {'aboutus_instance': aboutus_instance[0]})


class SpecialTeam(LoginRequiredMixin, TemplateView):
    template_name = 'superadmin/special_team.html'


class ProductPurchased(LoginRequiredMixin, TemplateView):
    template_name = 'superadmin/product-purchased.html'


class ProductsView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        product_category = ProductCategory.objects.all()
        vendors = Vendor.objects.all()
        context = {
            'categories': product_category,
            'vendors': vendors,
        }
        return render(request, 'superadmin/ecommerce-products.html', context)


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
        return render(self.request, 'superadmin/ecommerce-product-update.html', context)

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
        return redirect('/superadmin/products/')


class AddCategoryView(LoginRequiredMixin, View):
    template_name = 'superadmin/add-category.html'

    def get(self, request):
        departments = Departments.objects.all()
        return render(self.request, self.template_name, {'departments': departments})


class CategoryView(LoginRequiredMixin, View):
    template_name = 'superadmin/product-category.html'

    def get(self, request):
        departments = Departments.objects.all()
        return render(self.request, self.template_name, {'departments': departments})


class AddSubCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        product_category = ProductCategory.objects.all()
        context = {
            'product_category': product_category
        }
        return render(request, 'superadmin/add-sub-category.html', context)


class SubCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        product_category = ProductCategory.objects.all()
        context = {
            'product_category': product_category
        }
        return render(request, 'superadmin/product-sub-category.html', context)


class AddMiniCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        sub_category = ProductSubCategory.objects.all()
        context = {
            'sub_category': sub_category
        }
        return render(request, 'superadmin/add-mini-category.html', context)


class MiniCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        sub_category = ProductSubCategory.objects.all()
        context = {
            'sub_category': sub_category
        }
        return render(request, 'superadmin/product-mini-category.html', context)


class AddBrandView(VendorCheck, TemplateView):
    template_name = 'superadmin/add-brand.html'

class ManageBrandView(VendorCheck, TemplateView):
    template_name = 'superadmin/manage-brand.html'


class SalesReportView(LoginRequiredMixin, TemplateView):
    template_name = 'superadmin/monthly-report.html'


class VendorView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        vendor_list = Vendor.objects.filter(~Q(status="Pending"))
        context = {
            'vendor_list': vendor_list
        }
        template_name = 'superadmin/vendor-list.html'
        return render(request, template_name,context)


class VendorInformationShow(TemplateView):
    template_name = 'vendor/vendor-information-show.html'


class VendorApplicationView(LoginRequiredMixin, View):
    template_name = 'superadmin/vendor-applications.html'

    def get(self, request):
        vendor_list = Vendor.objects.filter(status='Pending')
        context = {
            'vendor_list': vendor_list
        }
        return render(request, self.template_name, context)


class VendorDetailsView(View):
    def get(self, request, id):
        vendor_details = Vendor.objects.get(pk=id)
        context = {
            'vendor_details': vendor_details
        }
        template_name = 'superadmin/vendor-details.html'
        return render(request, template_name, context)


class Contact(View):
    def get(self, request):
        contactus_instance = ContactUs.objects.all()
        template_name = 'superadmin/contactus.html'
        return render(self.request, template_name, {'contactus_instance': contactus_instance[0]})


class PoliciesView(TemplateView):
    template_name = 'superadmin/policies.html'


class FAQView(TemplateView):
    template_name = 'superadmin/faq.html'



class AddPolicyView(View):
    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        CompanyPolicy.objects.create(
            title=title,
            description=description
        )
        return redirect('/superadmin/policies/')


class UpdatePolicyView(View):
    def post(self, request):
        id = request.POST.get('id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        CompanyPolicy.objects.filter(pk=id).update(
            title=title,
            description=description
        )
        return redirect('/superadmin/policies/')


class AgentApplicationView(View):
    def get(self, request):
        agent_list = BusinessAgentProfile.objects.filter(status="Pending")
        context = {
            'agent_list': agent_list
        }
        template_name = 'superadmin/agent-applications.html'
        return render(request, template_name, context)


class AgentListView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        agent_list = BusinessAgentProfile.objects.filter(~Q(status="Pending"))
        context = {
            'agent_list': agent_list
        }
        template_name = 'superadmin/agent-list.html'
        return render(request, template_name,context)


class AgentDetailsView(View):
    def get(self, request, id):
        agent_details = BusinessAgentProfile.objects.get(pk=id)
        context = {
            'agent_details': agent_details
        }
        template_name = 'superadmin/agent-details.html'
        return render(request, template_name, context)


class ChangeAgentStatus(View):
    def get(self, request, pk, status):
        if request.user.is_admin:
            agent = BusinessAgentProfile.objects.get(pk=pk)
            agent.status = status
            agent.save()
            messages.success(request, 'Successfully updated')
            return redirect('/superadmin/agent-list/')

        else:
            messages.error(request, 'You do not have permission to perform this action')
            return redirect('/superadmin/')


class CreateVendorUser(View):
    def get(self, request, pk, status):
        if request.user.is_admin:
            vendor = Vendor.objects.get(pk=pk)
            vendor.status = status
            vendor.save()
            messages.success(request, 'Successfully updated')
            return redirect('/superadmin/vendor-list/')

        else:
            messages.error(request, 'You do not have permission to perform this action')
            return redirect('/superadmin/vendor-list/')
