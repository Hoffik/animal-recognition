# Generated by Django 2.1.7 on 2019-04-13 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0016_auto_20190413_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='file_type',
            field=models.CharField(choices=[('i', 'image'), ('a', 'audio'), ('v', 'video')], max_length=1),
        ),
    ]