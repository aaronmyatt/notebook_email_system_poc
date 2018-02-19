from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from login import urls as login_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include(login_urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns