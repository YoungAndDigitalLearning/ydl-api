# Generated by Django 2.0.7 on 2018-07-09 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_answer_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['order']},
        ),
    ]