# Generated by Django 4.0 on 2021-12-30 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_user_date_joined_alter_user_last_login'),
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('address', models.TextField(null=True)),
                ('mobile_number', models.CharField(max_length=11, unique=True)),
                ('_intrest_status', models.BooleanField(default=False)),
                ('intrest_rate', models.FloatField(default=0)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
            ],
        ),
    ]