from django.db import models
from django.core.exceptions import ValidationError


# ─────────────────────────────────────────────────────────────
# SITE SETTINGS  (singleton — only one row)
# ─────────────────────────────────────────────────────────────
class SiteSettings(models.Model):
    """Global site settings editable from the admin."""

    # Brand
    business_name   = models.CharField(max_length=100, default='KeyGuy Boss D')
    tagline         = models.CharField(max_length=200, default='Mobile Key Specialist')
    trading_as      = models.CharField(max_length=200, default='BOSS D trading as KeyGuy Centurion',
                                       help_text='Shown in footer legal line')

    # Contact
    phone_primary   = models.CharField(max_length=30, default='084 815 7329',
                                       help_text='Main phone number shown everywhere')
    phone_secondary = models.CharField(max_length=30, blank=True, default='076 827 4530',
                                       help_text='Second number (optional)')
    whatsapp_number = models.CharField(max_length=20, default='27848157329',
                                       help_text='International format without + e.g. 27848157329')
    email           = models.EmailField(default='keyesdiagnosis@gmail.com')
    location        = models.CharField(max_length=100, default='Centurion, Pretoria')

    # Hero section
    hero_heading_1  = models.CharField(max_length=100, default='Lost Your Car Key?')
    hero_heading_2  = models.CharField(max_length=100, default='We Come To You.')
    hero_subtext    = models.TextField(
        default='Professional mobile car key programming, replacement, cutting '
                'and diagnostics across Centurion & Pretoria. On your doorstep '
                '— no towing, no dealership.')
    hero_badge_text = models.CharField(max_length=100, default='Available Today · Mobile Service')
    hero_image_url  = models.URLField(
        blank=True,
        default='https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1920&q=85',
        help_text='Paste any image URL, or leave blank and upload hero_image below')
    hero_image      = models.ImageField(upload_to='hero/', blank=True, null=True,
                                        help_text='Upload overrides the URL above')

    # Stats bar
    stat_jobs_done       = models.PositiveIntegerField(default=500)
    stat_makes_covered  = models.PositiveIntegerField(default=50)
    stat_areas_served   = models.PositiveIntegerField(default=8)
    stat_rating_label   = models.CharField(max_length=20, default='5★')

    # SEO
    meta_title       = models.CharField(max_length=160,
                                        default='KeyGuy Boss D | Mobile Car Key Programming, Replacement & Diagnostics')
    meta_description = models.TextField(
        default='Mobile car key programming, replacement, cutting and diagnostics '
                'in Centurion and Pretoria. Fast on-site help for all makes and models. '
                'Call or WhatsApp 084 815 7329.')

    # Operating hours
    operating_hours = models.CharField(max_length=100, default='Mon–Sat · Fast response')

    class Meta:
        verbose_name        = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.business_name

    def save(self, *args, **kwargs):
        # Enforce singleton
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def whatsapp_url(self):
        msg = 'Hi%20KeyGuy%2C%20I%20need%20help%20with%20my%20car%20key.'
        return f'https://wa.me/{self.whatsapp_number}?text={msg}'

    def phone_primary_url(self):
        digits = ''.join(c for c in self.phone_primary if c.isdigit())
        return f'tel:+27{digits[-9:]}'

    def phone_secondary_url(self):
        if not self.phone_secondary:
            return ''
        digits = ''.join(c for c in self.phone_secondary if c.isdigit())
        return f'tel:+27{digits[-9:]}'

    def hero_bg(self):
        if self.hero_image:
            return self.hero_image.url
        return self.hero_image_url


# ─────────────────────────────────────────────────────────────
# SERVICES
# ─────────────────────────────────────────────────────────────
class Service(models.Model):
    ICON_CHOICES = [
        ('key',        'Key'),
        ('cpu',        'CPU / Chip'),
        ('scissors',   'Scissors / Cutting'),
        ('car',        'Car'),
        ('wrench',     'Wrench'),
        ('pin',        'Location Pin'),
        ('diagnostics','Diagnostics'),
        ('shield',     'Shield'),
    ]
    title       = models.CharField(max_length=100)
    description = models.TextField()
    icon        = models.CharField(max_length=20, choices=ICON_CHOICES, default='key')
    order       = models.PositiveIntegerField(default=0, help_text='Lower = shown first')
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name        = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────────────────────
# TESTIMONIALS / REVIEWS
# ─────────────────────────────────────────────────────────────
class Testimonial(models.Model):
    author_name  = models.CharField(max_length=100)
    location     = models.CharField(max_length=100, blank=True, help_text='e.g. Centurion')
    service_used = models.CharField(max_length=100, blank=True, help_text='e.g. Key replacement')
    body         = models.TextField()
    rating       = models.PositiveSmallIntegerField(default=5, choices=[(i, f'{i} stars') for i in range(1, 6)])
    is_active    = models.BooleanField(default=True)
    order        = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']
        verbose_name        = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f'{self.author_name} — {self.rating}★'

    def initials(self):
        parts = self.author_name.split()
        return ''.join(p[0].upper() for p in parts[:2])

    def stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)


# ─────────────────────────────────────────────────────────────
# SERVICE AREAS
# ─────────────────────────────────────────────────────────────
class ServiceArea(models.Model):
    name      = models.CharField(max_length=100)
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name        = 'Service Area'
        verbose_name_plural = 'Service Areas'

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────────────────────
# FAQ
# ─────────────────────────────────────────────────────────────
class FAQ(models.Model):
    question  = models.CharField(max_length=255)
    answer    = models.TextField()
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name        = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


# ─────────────────────────────────────────────────────────────
# GALLERY VALIDATORS
# ─────────────────────────────────────────────────────────────
def validate_image_size(image):
    max_mb = 2
    if image.size > max_mb * 1024 * 1024:
        raise ValidationError(f'Image file too large. Maximum size is {max_mb}MB. Your file is {image.size / 1024 / 1024:.1f}MB.')

MAX_GALLERY_ITEMS = 50

def validate_gallery_limit(value):
    from core.models import GalleryImage
    count = GalleryImage.objects.count()
    if count >= MAX_GALLERY_ITEMS:
        raise ValidationError(f'Gallery limit reached. Maximum {MAX_GALLERY_ITEMS} items allowed. Please delete an item before adding a new one.')


# ─────────────────────────────────────────────────────────────
# GALLERY
# ─────────────────────────────────────────────────────────────
class GalleryImage(models.Model):
    image     = models.ImageField(upload_to='gallery/', blank=True, null=True, validators=[validate_image_size])
    image_url = models.URLField(blank=True, help_text='Or paste an image URL if not uploading a file')
    video_url = models.TextField(
        blank=True,
        help_text='Paste a YouTube URL or the full embed code from YouTube (Share → Embed). Leave blank for images.'
    )
    caption   = models.CharField(max_length=200, blank=True)
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name        = 'Gallery Item'
        verbose_name_plural = 'Gallery Items'

    def __str__(self):
        return self.caption or f'Item {self.pk}'

    def clean(self):
        # Enforce 50 item limit on new items only
        if not self.pk:
            count = GalleryImage.objects.count()
            if count >= MAX_GALLERY_ITEMS:
                raise ValidationError(f'Gallery limit reached. Maximum {MAX_GALLERY_ITEMS} items allowed. Please delete an existing item first.')

    def is_video(self):
        return bool(self.video_url)

    def src(self):
        if self.image:
            return self.image.url
        return self.image_url

    def _extract_video_id(self):
        """Extract YouTube video ID from any YouTube URL or iframe tag."""
        import re
        url = self.video_url.strip()
        # Extract src from iframe tag if full iframe was pasted
        # Use a simple split approach to avoid quote conflicts in regex
        if '<iframe' in url and 'src=' in url:
            part = url.split('src=')[1]
            quote = part[0]
            url = part[1:part.index(quote, 1)]
        # Match video ID from any YouTube URL format
        match = re.search(r'(?:youtube\.com/(?:embed/|watch\?v=|shorts/)|youtu\.be/)([\w-]{11})', url)
        return match.group(1) if match else None

    def video_link(self):
        """Return a direct YouTube watch URL for opening in a new tab."""
        vid = self._extract_video_id()
        if vid:
            return f"https://www.youtube.com/watch?v={vid}"
        return self.video_url

    def thumbnail_url(self):
        """Return YouTube high-quality thumbnail image URL."""
        vid = self._extract_video_id()
        if vid:
            return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
        return ""

    def embed_url(self):
        """Return embed URL (kept for backwards compatibility)."""
        vid = self._extract_video_id()
        if vid:
            return f"https://www.youtube.com/embed/{vid}?rel=0&modestbranding=1"
        return self.video_url


# ─────────────────────────────────────────────────────────────
# QUOTE / CONTACT REQUESTS
# ─────────────────────────────────────────────────────────────
class QuoteRequest(models.Model):
    STATUS_CHOICES = [
        ('new',         'New'),
        ('contacted',   'Contacted'),
        ('completed',   'Completed'),
        ('closed',      'Closed'),
    ]
    name        = models.CharField(max_length=100)
    phone       = models.CharField(max_length=30)
    vehicle     = models.CharField(max_length=150, blank=True)
    service     = models.CharField(max_length=100, blank=True)
    area        = models.CharField(max_length=100, blank=True)
    message     = models.TextField(blank=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at  = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True, help_text='Internal notes (not shown to customer)')

    class Meta:
        ordering = ['-created_at']
        verbose_name        = 'Quote Request'
        verbose_name_plural = 'Quote Requests'

    def __str__(self):
        return f'{self.name} — {self.phone} ({self.created_at.strftime("%d %b %Y")})'
