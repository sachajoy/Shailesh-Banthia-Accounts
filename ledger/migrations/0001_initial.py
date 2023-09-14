# Generated by Django 4.0 on 2022-01-07 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('address', models.TextField(null=True)),
                ('mobile_number', models.CharField(max_length=11)),
                ('intrest_status', models.BooleanField(default=False)),
                ('intrest_rate', models.FloatField(default=0)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
            ],
        ),
        migrations.CreateModel(
            name='Firm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('abs', models.CharField(max_length=40, unique=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
            ],
        ),
        migrations.CreateModel(
            name='Trancation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('remarks', models.TextField(blank=True, null=True)),
                ('date', models.TextField()),
                ('booking_date', models.DateField()),
                ('passenger_list', models.TextField(null=True)),
                ('verifed', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ledger.client')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
                ('firm', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ledger.firm')),
            ],
            options={
                'ordering': ['booking_date'],
                'permissions': (('view_ledger', 'Can View Ledger'),),
            },
        ),
        migrations.CreateModel(
            name='SelectedPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
            ],
        ),
    ]