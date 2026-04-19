from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, Service, Testimonial, ServiceArea, FAQ, GalleryImage, QuoteRequest


# ─────────────────────────────────────────────────────────────
# SITE SETTINGS  (singleton admin)
# ─────────────────────────────────────────────────────────────
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🏢 Business Identity', {
            'fields': ('business_name', 'tagline', 'trading_as'),
        }),
        ('📞 Contact Details', {
            'fields': ('phone_primary', 'phone_secondary', 'whatsapp_number', 'email', 'location'),
            'description': 'These appear in the top bar, contact section and footer.',
        }),
        ('🦸 Hero Section', {
            'fields': ('hero_heading_1', 'hero_heading_2', 'hero_subtext',
                       'hero_badge_text', 'hero_image_url', 'hero_image'),
            'description': 'Upload an image OR paste a URL. Uploaded image takes priority.',
        }),
        ('📊 Stats Bar', {
            'fields': ('stat_keys_replaced', 'stat_makes_covered',
                       'stat_areas_served', 'stat_rating_label'),
        }),
        ('🕐 Operations', {
            'fields': ('operating_hours',),
        }),
        ('🔍 SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        # Prevent creating a second row
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Redirect list → change page for the singleton
        from django.shortcuts import redirect
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        return redirect(f'/admin/core/sitesettings/{obj.pk}/change/')


# ─────────────────────────────────────────────────────────────
# SERVICES
# ─────────────────────────────────────────────────────────────
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ('title', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('is_active',)
    search_fields = ('title',)
    ordering      = ('order',)


# ─────────────────────────────────────────────────────────────
# TESTIMONIALS
# ─────────────────────────────────────────────────────────────
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display  = ('author_name', 'location', 'service_used', 'rating', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('rating', 'is_active')
    search_fields = ('author_name', 'body')


# ─────────────────────────────────────────────────────────────
# SERVICE AREAS
# ─────────────────────────────────────────────────────────────
@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display  = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')


# ─────────────────────────────────────────────────────────────
# FAQ
# ─────────────────────────────────────────────────────────────
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display  = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('question', 'answer')


# ─────────────────────────────────────────────────────────────
# GALLERY
# ─────────────────────────────────────────────────────────────
@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display  = ('thumb', 'caption', 'item_type', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Image', {
            'fields': ('image', 'image_url'),
            'description': 'Upload an image file OR paste an image URL. Leave both blank if adding a video.',
        }),
        ('Video (YouTube or TikTok)', {
            'fields': ('video_url',),
            'description': 'Paste a YouTube or TikTok link. Example: https://www.youtube.com/watch?v=XXXX',
        }),
        ('Details', {
            'fields': ('caption', 'order', 'is_active'),
        }),
    )

    def thumb(self, obj):
        if obj.is_video():
            return format_html('<span style="font-size:1.4rem;" title="{}">▶️</span>', obj.video_url)
        src = obj.src()
        if src:
            return format_html('<img src="{}" style="height:50px;border-radius:6px;">', src)
        return '—'
    thumb.short_description = 'Preview'

    def item_type(self, obj):
        if obj.is_video():
            url = obj.video_url
            if 'youtube' in url or 'youtu.be' in url:
                return '▶ YouTube'
            if 'tiktok' in url:
                return '▶ TikTok'
            return '▶ Video'
        return '🖼 Image'
    item_type.short_description = 'Type'


# ─────────────────────────────────────────────────────────────
# QUOTE REQUESTS
# ─────────────────────────────────────────────────────────────
@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display  = ('name', 'phone', 'vehicle', 'service', 'area', 'status', 'created_at')
    list_editable = ('status',)
    list_filter   = ('status', 'service')
    search_fields = ('name', 'phone', 'vehicle', 'message')
    readonly_fields = ('name', 'phone', 'vehicle', 'service', 'area', 'message', 'created_at')
    fieldsets = (
        ('Customer Request', {
            'fields': ('name', 'phone', 'vehicle', 'service', 'area', 'message', 'created_at'),
        }),
        ('Admin', {
            'fields': ('status', 'admin_notes'),
        }),
    )

    def has_add_permission(self, request):
        return False  # Requests come from the website form only
