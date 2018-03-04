# Generated by Django 2.0.2 on 2018-03-04 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now_add=True)),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True)),
                ('usd', models.DecimalField(decimal_places=4, default=0, max_digits=16, verbose_name='USD')),
                ('eur', models.DecimalField(decimal_places=4, default=0, max_digits=16, verbose_name='EUR')),
                ('btc', models.DecimalField(decimal_places=8, default=0, max_digits=16, verbose_name='BTC')),
                ('ltc', models.DecimalField(decimal_places=8, default=0, max_digits=16, verbose_name='LTC')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='account_account_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='account_account_updated_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='account_account_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
