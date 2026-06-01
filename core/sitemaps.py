from datetime import date

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return ['home', 'services', 'gallery', 'about', 'reviews', 'contact']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return {
            'home': 1.0,
            'services': 0.9,
            'contact': 0.9,
            'about': 0.8,
            'gallery': 0.7,
            'reviews': 0.7,
        }.get(item, 0.5)

    def changefreq(self, item):
        return {
            'home': 'daily',
            'services': 'monthly',
            'contact': 'monthly',
            'about': 'monthly',
            'gallery': 'weekly',
            'reviews': 'weekly',
        }.get(item, 'weekly')

    def lastmod(self, item):
        return date.today()
