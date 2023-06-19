from django.urls import path

from superadmin import views

urlpatterns = [

    path('', views.SuperAdminIndexView.as_view(), name='superadmin-index'),
    path('static-upload/', views.LogoUpload.as_view(), name='static-upload'),
    path('main-banner-upload/', views.MainBannerUpload.as_view(), name='main-banner'),
    path('promotional-upload/', views.PromotionalBannerUpload.as_view(), name='promotional-banner'),
    path('invoice/', views.Invoice.as_view(), name='invoice'),
    path('main-slider/', views.ViewMainSlider.as_view(), name='main-slider'),
    path('memberlist/', views.MemberList.as_view(), name='memberlist'),
    path('aboutus/', views.AboutusView.as_view(), name='aboutus'),
    path('special-team/', views.SpecialTeam.as_view(), name='special-team'),
    path('contactus/', views.Contact.as_view(), name='contact'),
    path('policies/', views.PoliciesView.as_view(), name='policies'),
    path('add-policy/', views.AddPolicyView.as_view(), name='add-policy'),
    path('update-policy/', views.UpdatePolicyView.as_view(), name='update-policy'),
    path('faq-admin/', views.FAQView.as_view(), name='faq-admin'),
    path('purchased/', views.ProductPurchased.as_view(), name='purchased'),
    path('products/', views.ProductsView.as_view(), name='products'),
    path('product-details/<slug:slug>/', views.ProductEditView.as_view(), name='super_admin_edit_product'),
    path('add-category/', views.AddCategoryView.as_view(), name='add-category'),
    path('add-sub-category/', views.AddSubCategoryView.as_view(), name='add-sub-category'),
    path('add-mini-category/', views.AddMiniCategoryView.as_view(), name='add-mini-category'),
    path('category/', views.CategoryView.as_view(), name='category'),
    path('sub-category/', views.SubCategoryView.as_view(), name='sub-category'),
    path('mini-category/', views.MiniCategoryView.as_view(), name='mini-category'),

    path('add-brand/', views.AddBrandView.as_view(), name='add-brand'),
    path('manage-brand/', views.ManageBrandView.as_view(), name='view-brand'),

    path('sales-report/', views.SalesReportView.as_view(), name='sales-report'),
    path('vendor-list/', views.VendorView.as_view(), name='vendor-list'),
    path('vendor-application/', views.VendorApplicationView.as_view(), name='vendor-application'),
    path('vendor-info/', views.VendorInformationShow.as_view(), name='vendor-info'),
    path('vendor-details/<id>/', views.VendorDetailsView.as_view(), name="vendor-details"),

    path('agent-application/', views.AgentApplicationView.as_view(), name='agent-application'),
    path('agent-list/', views.AgentListView.as_view(), name='agent-list'),
    path('agent-details/<id>/', views.AgentDetailsView.as_view(), name="agent-details"),
    path('change-agent-status/<int:pk>/<status>/', views.ChangeAgentStatus.as_view(), name="change-agent-status"),


    path('agent-application/', views.AgentApplicationView.as_view(), name="agent-application"),
    path('agent-details/<id>/', views.AgentDetailsView.as_view(), name="agent-details"),
    path('change-vendor-status/<int:pk>/<status>/', views.CreateVendorUser.as_view(), name="change-vendor-status"),

]
