from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/', include('data_type_conversion_app.urls')),  # Include your app's URLs
]
