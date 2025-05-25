# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.student_login_view, name='student_login'),
    path("verify-otp/", views.otp_verification_view, name='otp_verification'),
    path("logout/", views.logout_view, name='logout'),
    path('filter-members/', views.filter_members, name='filter_members'),
]