# Generated by Django 3.2 on 2021-04-19 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piazza', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='owner',
        ),
    ]