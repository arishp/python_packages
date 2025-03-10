from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('data_visualization/', include('data_visualization.urls')),
    path('admin/', admin.site.urls),
]