# Generated by Django 3.2.19 on 2023-08-12 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0006_alter_parcel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcel',
            name='packed_on',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='status',
            field=models.CharField(default='In China WH', editable=False, max_length=20),
        ),
    ]
