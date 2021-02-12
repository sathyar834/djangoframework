# Generated by Django 3.1.5 on 2021-02-11 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0003_auto_20210211_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='createscp',
            name='Document_name',
        ),
        migrations.RemoveField(
            model_name='createscp',
            name='SCP_Description',
        ),
        migrations.RemoveField(
            model_name='createscp',
            name='SCP_Name',
        ),
        migrations.AddField(
            model_name='createscp',
            name='Documentname',
            field=models.CharField(default='', editable=False, max_length=30),
        ),
        migrations.AddField(
            model_name='createscp',
            name='SCPDescription',
            field=models.CharField(default='', editable=False, max_length=30),
        ),
        migrations.AddField(
            model_name='createscp',
            name='SCPName',
            field=models.CharField(default='', editable=False, max_length=30),
        ),
    ]
