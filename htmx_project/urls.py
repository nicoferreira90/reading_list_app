from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

from reading.views import AboutPageView

urlpatterns = [
    path("kbzon/", admin.site.urls),
    path("", include("reading.urls")),
    path("accounts/", include("allauth.urls")),
    path("about/", AboutPageView.as_view(), name="about_page"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
