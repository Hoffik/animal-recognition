# Generated by Django 2.2.2 on 2019-09-03 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='imagename',
            field=models.CharField(default='default_image', max_length=50),
            preserve_default=False,
        ),
    ]
