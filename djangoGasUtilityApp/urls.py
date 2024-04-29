# urls.py
from django.urls import path
from todo import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('submit-service-request/', views.submit_service_request, name='submit_service_request'),
    path('track-service-request/<int:request_id>/', views.track_service_request, name='track_service_request'),
    path('manage-support-tickets/', views.manage_support_tickets, name='manage_support_tickets'),
    path('update-service-request-status/<int:request_id>/', views.update_service_request_status, name='update_service_request_status'),
]
