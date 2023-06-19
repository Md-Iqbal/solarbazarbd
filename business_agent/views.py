from inventory_api.models import Departments, ProductCategory
from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import BusinessAgentProfile

from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from user_auth.models import User

from . models import BusinessAgentProfile
# Create your views here.
from .serializers import AgentSerializer


class BusinessAgentIndex(TemplateView):
    template_name = 'business_agent/business-agent-index.html'


class BecomeAgent(TemplateView):
    def get(self, request):
        departments = Departments.objects.all()
        category = ProductCategory.objects.filter(is_active=True)
        context = {
            'categories': category,
            'departments': departments,
        }
        return render(request, 'become-vendor.html', context)


class AgentList(generics.ListCreateAPIView):
    permission_classes = ()
    serializer_class = AgentSerializer
    queryset = BusinessAgentProfile.objects.all()

    def perform_create(self, serializer):
        u_email = self.request.data['email']
        u_pass = self.request.data['password']
        if User.objects.filter(email=u_email).exists():
            raise ValidationError('Agent exists with this email. Please try with another one')
        else:
            if serializer.is_valid():
                u = User.objects.create(username=u_email, email=u_email, is_agent=True)
                u.set_password(u_pass)
                u.save()
            else:
                u=None
            serializer.save(user=u)





def businessAgentRegistration(request):
    if request.method == 'POST':
        business_center_id = request.POST['business_center_id']
        full_name = request.POST['full_name']
        father_name = request.POST['father_name']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        profile_image = request.POST['profile_image']
        nid_front = request.POST['nid_front']
        nid_back = request.POST['nid_back']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        reference_code = str('BA-'+full_name.split(" ")[-1]+phone[-3:]).upper()
        print(reference_code)

        if BusinessAgentProfile.objects.filter(phone=phone).exists():
            messages.error(request, 'Already have an account with this phone ')
            return redirect( 'login-agent')

        else:
            try:
                agent_info = BusinessAgentProfile(
                    business_center_id=business_center_id,
                    full_name=full_name,
                    father_name=father_name,
                    address=address,
                    email=email,
                    phone=phone,
                    profile_image=profile_image,
                    nid_front=nid_front,
                    nid_back=nid_back,
                    password=password,
                    confirm_password=confirm_password,
                    reference_code=reference_code
                )
                agent_info.save()
            except Exception as e:
                msg = 'Failed! '+str(e)
                messages.success(request, msg)
                print(e)
                return redirect('login-agent')

        messages.success(request, 'Successfully submitted')
        return redirect('/')



class AgentListView(View):
    def get(self, request):
        business_aget_list = BusinessAgentProfile.objects.filter(status="Active")
        context = {
            'business_aget_list': business_aget_list
        }
        return render(request,'business_agent/ecommerce-sellers.html', context )

# class AgentApplicationView(View):
#     def get(self,request):
#         agent_list = BusinessAgentProfile.objects.all()
#         context ={
#             'agent_list': agent_list
#         }
#         template_name = 'business_agent/agent-applications.html'
#         return render(request, template_name, context)
#
#
# class AgentDetailsView(View):
#     def get(self,request, id):
#         agent_details = BusinessAgentProfile.objects.get(pk=id)
#         context = {
#             'agent_details': agent_details
#         }
#         template_name = 'business_agent/agent-details.html'
#         return render(request,template_name,context)

class Authuser(TemplateView):
    template_name = 'business_agent/auth-login.html'


class CreateAgentUser(View):
    def get(self, request, phone):
        user = User.objects.filter(username=phone)
        if not user:
            b = BusinessAgentProfile.objects.get(phone=phone)
            user = User.objects.create_user(username=phone,password=b.password)
            user.save()

            b.status='Active'
            b.user = user
            b.save()
            messages.success(request, 'Successfully submitted')
            return redirect('/')

        else:
            messages.error(request, 'Already have an account with this phone ')
            return redirect('agent-registration')








