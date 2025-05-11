from django.contrib import admin
from django.urls import path, include
from core.views import custom_404_dev 


admin.site.site_header = "Voting System Admin"
admin.site.site_title = "Voting System Admin Portal"
admin.site.index_title = "Welcome to the Voting System Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('core.urls')),
]

handler404 = custom_404_dev
