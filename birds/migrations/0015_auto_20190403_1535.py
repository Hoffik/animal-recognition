# Generated by Django 2.1.7 on 2019-04-03 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0014_remove_record_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='identifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='right',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rights', to=settings.AUTH_USER_MODEL),
        ),
    ]
