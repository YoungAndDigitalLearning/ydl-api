# Generated by Django 2.0.7 on 2018-07-09 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20180709_1800'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-order']},
        ),
    ]
