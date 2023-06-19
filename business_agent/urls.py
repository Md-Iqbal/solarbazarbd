
from django.urls import path

from business_agent import views

urlpatterns = [

    path('', views.BusinessAgentIndex.as_view(), name="business-agent"),
    path('become-agent/', views.BecomeAgent.as_view(), name="become-agent"),
    path('agent-registration/', views.businessAgentRegistration, name="agent-registration"),
    # path('agent-list/', views.AgentListView.as_view(), name="agent-list"),
    # path('agent-application/', views.AgentApplicationView.as_view(), name="agent-application"),
    # path('agent-details/<id>/', views.AgentDetailsView.as_view(), name="agent-details"),
    path('agent-auth/', views.Authuser.as_view(), name="agent-auth"),
    path('create-agent-user/<phone>/', views.CreateAgentUser.as_view(), name="create-agent-user"),

    path('agent-list/', views.AgentList.as_view(), name='Agent_list'),

    ]