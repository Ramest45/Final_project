# Generated by Django 5.0.2 on 2024-10-12 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nouapp', '0010_complaints_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complaints',
            old_name='feed',
            new_name='comp',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='comp',
            new_name='feed',
        ),
    ]