# Generated by Django 5.0.7 on 2024-07-15 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_sd_access", "0003_ippool"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fabricsite",
            name="ip_prefixes",
            field=models.ManyToManyField(to="netbox_sd_access.ippool"),
        ),
    ]
