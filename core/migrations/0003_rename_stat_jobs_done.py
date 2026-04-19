from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_galleryimage_video_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sitesettings',
            old_name='stat_keys_replaced',
            new_name='stat_jobs_done',
        ),
    ]
