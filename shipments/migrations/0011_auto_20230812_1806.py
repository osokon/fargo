# Generated by Django 3.2.19 on 2023-08-12 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0010_alter_parcel_received_on'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parcel',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='shipment',
            options={'ordering': ['-id']},
        ),
    ]
