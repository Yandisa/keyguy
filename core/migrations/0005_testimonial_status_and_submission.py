from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_stat_jobs_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial',
            name='status',
            field=models.CharField(
                choices=[('pending', 'Pending Approval'), ('approved', 'Approved'), ('rejected', 'Rejected')],
                default='approved',
                help_text='Only approved reviews show on the site',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='submitted_by_customer',
            field=models.BooleanField(default=False, help_text='Submitted via the website form'),
        ),
    ]
