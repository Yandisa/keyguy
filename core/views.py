from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings as django_settings

from .models import SiteSettings, Service, Testimonial, ServiceArea, FAQ, GalleryImage
from .forms import QuoteForm


def _common_context():
    """Context shared across all pages."""
    return {
        'services': Service.objects.filter(is_active=True),
        'areas':    ServiceArea.objects.filter(is_active=True),
    }


def home(request):
    ctx = _common_context()
    ctx.update({
        'reviews': Testimonial.objects.filter(is_active=True, status='approved').order_by('order', '-id')[:6],
        'faqs':    FAQ.objects.filter(is_active=True),
        'gallery': GalleryImage.objects.filter(is_active=True)[:9],  # home shows latest 9
        'form':    QuoteForm(),
    })

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            site = SiteSettings.get()
            quote = form.save()
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
        ctx['form'] = form

    return render(request, 'core/home.html', ctx)


def services(request):
    ctx = _common_context()
    return render(request, 'core/services.html', ctx)


def gallery(request):
    ctx = _common_context()
    ctx['gallery'] = GalleryImage.objects.filter(is_active=True)
    return render(request, 'core/gallery.html', ctx)


def about(request):
    ctx = _common_context()
    ctx['faqs'] = FAQ.objects.filter(is_active=True)
    return render(request, 'core/about.html', ctx)


def reviews(request):
    ctx = _common_context()
    ctx['reviews'] = Testimonial.objects.filter(is_active=True, status='approved').order_by('order', '-id')
    ctx['review_submitted'] = False
    ctx['review_errors'] = None
    ctx['review_form_data'] = {}

    if request.method == 'POST' and request.POST.get('review_form'):
        author_name = request.POST.get('author_name', '').strip()
        body        = request.POST.get('body', '').strip()
        location    = request.POST.get('location', '').strip()
        service_used = request.POST.get('service_used', '').strip()
        rating      = request.POST.get('rating', '5')

        ctx['review_form_data'] = {
            'author_name': author_name,
            'body': body,
            'location': location,
        }

        if not author_name:
            ctx['review_errors'] = 'Please enter your name.'
        elif not body or len(body) < 20:
            ctx['review_errors'] = 'Please write a review of at least 20 characters.'
        else:
            Testimonial.objects.create(
                author_name=author_name,
                location=location,
                service_used=service_used,
                body=body,
                rating=int(rating) if rating.isdigit() else 5,
                status='pending',
                is_active=False,
                submitted_by_customer=True,
            )
            # Notify admin
            try:
                site = SiteSettings.get()
                send_mail(
                    subject=f'New review submitted by {author_name}',
                    message=f'Name: {author_name}\nRating: {rating}/5\nService: {service_used}\n\nReview:\n{body}\n\nApprove at /admin/core/testimonial/',
                    from_email=django_settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[site.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            ctx['review_submitted'] = True

    return render(request, 'core/reviews.html', ctx)


def contact(request):
    ctx = _common_context()
    ctx['form'] = QuoteForm()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            site = SiteSettings.get()
            quote = form.save()
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
            return redirect('contact')
        ctx['form'] = form

    return render(request, 'core/contact.html', ctx)
