from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return ['home', 'services', 'gallery', 'about', 'reviews', 'contact']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        priorities = {
            'home': 1.0,
            'services': 0.9,
            'contact': 0.9,
            'about': 0.8,
            'gallery': 0.7,
            'reviews': 0.7,
        }
        return priorities.get(item, 0.5)
