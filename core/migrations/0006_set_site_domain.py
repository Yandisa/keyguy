from django.db import migrations


def set_site_domain(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        pk=1,
        defaults={'domain': 'www.bossd.co.za', 'name': 'KeyGuy Boss D'}
    )


def revert(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_testimonial_status_and_submission'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(set_site_domain, revert),
    ]
