# Generated by Django 5.1.4 on 2025-01-20 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('c_auth', '0002_token'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Token',
            new_name='TokenModel',
        ),
        migrations.AlterModelOptions(
            name='tokenmodel',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='tokenmodel',
            table='token_table',
        ),
    ]
