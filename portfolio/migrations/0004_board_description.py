# Generated by Django 3.2 on 2021-04-20 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_auto_20210420_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
