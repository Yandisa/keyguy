from .models import SiteSettings, Testimonial


def site_settings(request):
    reviews_count = Testimonial.objects.filter(
        is_active=True, status='approved'
    ).count()
    return {
        'settings': SiteSettings.get(),
        'reviews_count': reviews_count,
    }
