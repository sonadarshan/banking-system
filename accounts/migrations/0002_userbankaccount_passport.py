# Generated by Django 3.2.9 on 2022-11-08 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbankaccount',
            name='passport',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
