from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='video_url',
            field=models.URLField(
                blank=True,
                help_text='Paste a YouTube or TikTok URL. Leave blank for images.'
            ),
        ),
    ]
