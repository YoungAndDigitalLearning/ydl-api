# Generated by Django 2.0.6 on 2018-06-21 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='root_post',
            new_name='parent_post',
        ),
    ]