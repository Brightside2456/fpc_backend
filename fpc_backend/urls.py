from django.contrib import admin
from django.urls import path, include, re_path
from djoser import urls as djurls
from c_auth import urls as c_auth_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include(c_auth_urls)),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
]
