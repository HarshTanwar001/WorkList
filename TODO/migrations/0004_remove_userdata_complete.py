# Generated by Django 4.1.6 on 2023-02-15 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TODO', '0003_remove_userdata_pwd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='complete',
        ),
    ]
