# Generated by Django 3.1.5 on 2021-02-11 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0004_auto_20210211_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachscp',
            name='AccountId',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='attachscp',
            name='SCPPolicyId',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='createscp',
            name='Documentname',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='createscp',
            name='SCPDescription',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='createscp',
            name='SCPName',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='listou',
            name='ParentIdlistou',
            field=models.TextField(max_length=30),
        ),
    ]