# Generated by Django 3.1.2 on 2021-02-03 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_network_scanningapiurl'),
    ]

    operations = [
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=300)),
                ('time', models.CharField(max_length=50)),
                ('device_serial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.device')),
            ],
        ),
    ]
