# Generated by Django 5.0.2 on 2024-10-08 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nouapp', '0003_contact'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='contact',
            new_name='tbl_contact',
        ),
    ]
