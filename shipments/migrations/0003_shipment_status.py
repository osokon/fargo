# Generated by Django 3.2.19 on 2023-08-09 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0002_parcel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='status',
            field=models.CharField(default='active', max_length=20),
            preserve_default=False,
        ),
    ]
