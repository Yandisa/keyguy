from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_stat_jobs_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryimage',
            name='video_url',
            field=models.TextField(
                blank=True,
                help_text='Paste a YouTube URL or the full embed code from YouTube (Share → Embed). Leave blank for images.'
            ),
        ),
    ]
