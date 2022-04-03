
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from Subapp01.sitemap import PostSitemap

sitemaps = {
    'posts':PostSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('Subapp01.urls')),
    path(
        'sitemap.xml',sitemap, {'sitemaps':sitemaps}, name='django.contrib.sitemaps.views.sitemap'
        )
]


urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
