# Generated by Django 3.2.19 on 2023-07-31 21:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DepletionAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('sms_count', models.PositiveIntegerField()),
                ('alerts', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SmsTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('text', models.CharField(max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('added_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SmsConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sms_enabled', models.BooleanField(default=False)),
                ('provider', models.CharField(default='nextsms', max_length=50)),
                ('sender_id', models.CharField(default='Skuli App', max_length=11)),
                ('headers_authorization', models.CharField(default='GDS', max_length=200)),
                ('live_endpoint', models.CharField(default='https://messaging-service.co.tz/api/sms/v1/text/single', max_length=100)),
                ('balance_endpoint', models.CharField(default='https://messaging-service.co.tz/api/sms/v1/balance', max_length=100)),
                ('delivery_status_endpoint', models.CharField(default='https://messaging-service.co.tz/api/sms/v1/reports?', max_length=100)),
                ('beem_sender_id', models.CharField(default='Skuli', max_length=11)),
                ('beem_headers_authorization', models.CharField(default='GDS', max_length=200)),
                ('beem_live_endpoint', models.CharField(default='GDS', max_length=100)),
                ('beem_balance_endpoint', models.CharField(default='GDS', max_length=100)),
                ('beem_delivery_status_endpoint', models.CharField(default='GDS', max_length=100)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('added_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('source', models.CharField(max_length=100)),
                ('destination', models.BigIntegerField()),
                ('text', models.CharField(max_length=1000)),
                ('mno', models.CharField(blank=True, max_length=20, null=True, verbose_name='Mobile Network Operator')),
                ('sms_count', models.PositiveIntegerField(null=True)),
                ('delivery_status', models.CharField(max_length=100)),
                ('status_description', models.CharField(max_length=100)),
                ('messageId', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sent_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalSmsTemplate',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50)),
                ('text', models.CharField(max_length=1000)),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('added_by', django_currentuser.db.models.fields.CurrentUserField(blank=True, db_constraint=False, default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical sms template',
                'verbose_name_plural': 'historical sms templates',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSmsConfig',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('sms_enabled', models.BooleanField(default=False)),
                ('provider', models.CharField(default='nextsms', max_length=50)),
                ('sender_id', models.CharField(default='Skuli App', max_length=11)),
                ('headers_authorization', models.CharField(default='GDS', max_length=200)),
                ('live_endpoint', models.CharField(default='https://messaging-service.co.tz/api/sms/v1/text/single', max_length=100)),
                ('balance_endpoint', models.CharField(default='https://messaging-service.co.tz/api/sms/v1/balance', max_length=100)),
                ('delivery_status_endpoint', models.CharField(default='https://messaging-service.co.tz/api/sms/v1/reports?', max_length=100)),
                ('beem_sender_id', models.CharField(default='Skuli', max_length=11)),
                ('beem_headers_authorization', models.CharField(default='GDS', max_length=200)),
                ('beem_live_endpoint', models.CharField(default='GDS', max_length=100)),
                ('beem_balance_endpoint', models.CharField(default='GDS', max_length=100)),
                ('beem_delivery_status_endpoint', models.CharField(default='GDS', max_length=100)),
                ('added_on', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('added_by', django_currentuser.db.models.fields.CurrentUserField(blank=True, db_constraint=False, default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical sms config',
                'verbose_name_plural': 'historical sms configs',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]