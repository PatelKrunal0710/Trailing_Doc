# Generated by Django 2.1 on 2019-07-18 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Processing', '0006_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileinfo',
            name='File_note',
            field=models.CharField(default='null', max_length=254),
            preserve_default=False,
        ),
    ]