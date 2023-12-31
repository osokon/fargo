# Generated by Django 3.2.19 on 2023-08-09 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_no', models.CharField(max_length=20)),
                ('owner', models.CharField(max_length=20)),
                ('owner_mobile', models.CharField(max_length=20)),
                ('weight', models.CharField(max_length=20)),
                ('received_on', models.DateField(blank=True, null=True)),
                ('shipped_on', models.DateField(blank=True, null=True)),
                ('shipment', models.DateField(blank=True, null=True)),
                ('landed_on', models.DateField(blank=True, null=True)),
                ('delivered_on', models.DateField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_no', models.CharField(max_length=20)),
                ('shipped_on', models.CharField(max_length=20)),
                ('eta', models.CharField(max_length=20)),
                ('received_on', models.DateField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
