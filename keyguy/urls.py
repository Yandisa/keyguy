from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse

from core.sitemaps import StaticViewSitemap


admin.site.site_header  = 'KeyGuy Centurion Admin'
admin.site.site_title   = 'KeyGuy Admin'
admin.site.index_title  = 'Site Management'


sitemaps = {
    'static': StaticViewSitemap,
}


def robots_txt(request):
    content = """User-agent: *
Allow: /
Disallow: /admin/

Sitemap: https://www.bossd.co.za/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
    path('', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
