from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(default='KeyGuy Boss D', max_length=100)),
                ('tagline', models.CharField(default='Mobile Key Specialist', max_length=200)),
                ('trading_as', models.CharField(default='BOSS D trading as KeyGuy Centurion', help_text='Shown in footer legal line', max_length=200)),
                ('phone_primary', models.CharField(default='084 815 7329', help_text='Main phone number shown everywhere', max_length=30)),
                ('phone_secondary', models.CharField(blank=True, default='076 827 4530', help_text='Second number (optional)', max_length=30)),
                ('whatsapp_number', models.CharField(default='27848157329', help_text='International format without + e.g. 27848157329', max_length=20)),
                ('email', models.EmailField(default='keyesdiagnosis@gmail.com', max_length=254)),
                ('location', models.CharField(default='Centurion, Pretoria', max_length=100)),
                ('hero_heading_1', models.CharField(default='Lost Your Car Key?', max_length=100)),
                ('hero_heading_2', models.CharField(default='We Come To You.', max_length=100)),
                ('hero_subtext', models.TextField(default='Professional mobile car key programming, replacement, cutting and diagnostics across Centurion & Pretoria. On your doorstep — no towing, no dealership.')),
                ('hero_badge_text', models.CharField(default='Available Today · Mobile Service', max_length=100)),
                ('hero_image_url', models.URLField(blank=True, default='https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1920&q=85', help_text='Paste any image URL, or leave blank and upload hero_image below')),
                ('hero_image', models.ImageField(blank=True, help_text='Upload overrides the URL above', null=True, upload_to='hero/')),
                ('stat_keys_replaced', models.PositiveIntegerField(default=500)),
                ('stat_makes_covered', models.PositiveIntegerField(default=50)),
                ('stat_areas_served', models.PositiveIntegerField(default=8)),
                ('stat_rating_label', models.CharField(default='5★', max_length=20)),
                ('meta_title', models.CharField(default='KeyGuy Boss D | Mobile Car Key Programming, Replacement & Diagnostics', max_length=160)),
                ('meta_description', models.TextField(default='Mobile car key programming, replacement, cutting and diagnostics in Centurion and Pretoria. Fast on-site help for all makes and models. Call or WhatsApp 084 815 7329.')),
                ('operating_hours', models.CharField(default='Mon–Sat · Fast response', max_length=100)),
            ],
            options={
                'verbose_name': 'Site Settings',
                'verbose_name_plural': 'Site Settings',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('icon', models.CharField(choices=[('key', 'Key'), ('cpu', 'CPU / Chip'), ('scissors', 'Scissors / Cutting'), ('car', 'Car'), ('wrench', 'Wrench'), ('pin', 'Location Pin'), ('diagnostics', 'Diagnostics'), ('shield', 'Shield')], default='key', max_length=20)),
                ('order', models.PositiveIntegerField(default=0, help_text='Lower = shown first')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
                'ordering': ['order', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=100)),
                ('location', models.CharField(blank=True, help_text='e.g. Centurion', max_length=100)),
                ('service_used', models.CharField(blank=True, help_text='e.g. Key replacement', max_length=100)),
                ('body', models.TextField()),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, '1 stars'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')], default=5)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonials',
                'ordering': ['order', '-id'],
            },
        ),
        migrations.CreateModel(
            name='ServiceArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Service Area',
                'verbose_name_plural': 'Service Areas',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'FAQ',
                'verbose_name_plural': 'FAQs',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='gallery/')),
                ('image_url', models.URLField(blank=True, help_text='Or paste a URL if not uploading a file')),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Gallery Image',
                'verbose_name_plural': 'Gallery Images',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='QuoteRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=30)),
                ('vehicle', models.CharField(blank=True, max_length=150)),
                ('service', models.CharField(blank=True, max_length=100)),
                ('area', models.CharField(blank=True, max_length=100)),
                ('message', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('new', 'New'), ('contacted', 'Contacted'), ('completed', 'Completed'), ('closed', 'Closed')], default='new', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('admin_notes', models.TextField(blank=True, help_text='Internal notes (not shown to customer)')),
            ],
            options={
                'verbose_name': 'Quote Request',
                'verbose_name_plural': 'Quote Requests',
                'ordering': ['-created_at'],
            },
        ),
    ]
