# Generated by Django 3.0.8 on 2020-07-15 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200714_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
