# Generated by Django 3.2 on 2021-04-20 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='card_url',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='task',
            name='label',
            field=models.CharField(max_length=200),
        ),
    ]
