# Generated by Django 5.1.4 on 2025-01-20 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('c_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('token', models.CharField(max_length=250)),
                ('expired', models.BooleanField(default=False)),
                ('use_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
