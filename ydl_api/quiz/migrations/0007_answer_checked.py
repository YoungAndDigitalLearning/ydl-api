# Generated by Django 2.0.7 on 2018-07-11 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_auto_20180709_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]