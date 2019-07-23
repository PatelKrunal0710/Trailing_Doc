# Generated by Django 2.1 on 2019-07-08 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Processing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileinfo',
            name='File_process',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='File_status',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='Proc_edate',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='Proc_sdate',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='Proc_userid',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='Qc_edate',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='Qc_process',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='Qc_sdate',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='Qc_userid',
            field=models.CharField(blank=True, max_length=254),
        ),
    ]
