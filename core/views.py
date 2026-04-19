from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings as django_settings

from .models import SiteSettings, Service, Testimonial, ServiceArea, FAQ, GalleryImage
from .forms import QuoteForm


def home(request):
    site     = SiteSettings.get()
    services = Service.objects.filter(is_active=True)
    reviews  = Testimonial.objects.filter(is_active=True)
    areas    = ServiceArea.objects.filter(is_active=True)
    faqs     = FAQ.objects.filter(is_active=True)
    gallery  = GalleryImage.objects.filter(is_active=True)

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save()
            # Try to send a notification email
            try:
                send_mail(
                    subject=f'New quote request from {quote.name}',
                    message=(
                        f'Name:    {quote.name}\n'
                        f'Phone:   {quote.phone}\n'
                        f'Vehicle: {quote.vehicle}\n'
                        f'Service: {quote.service}\n'
                        f'Area:    {quote.area}\n\n'
                        f'Message:\n{quote.message}'
                    ),
                    from_email=django_settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[site.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, 'Request received! We will be in touch shortly.')
            return redirect('home')
        # form errors fall through to template
    else:
        form = QuoteForm()

    return render(request, 'core/home.html', {
        'services': services,
        'reviews':  reviews,
        'areas':    areas,
        'faqs':     faqs,
        'gallery':  gallery,
        'form':     form,
    })
