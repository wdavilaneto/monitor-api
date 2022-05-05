# Generated by Django 3.2 on 2021-04-20 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_board_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField(blank=True, null=True)),
                ('pain', models.TextField(blank=True, null=True)),
                ('requirements', models.CharField(max_length=1000)),
                ('risks', models.CharField(max_length=1000)),
                ('quarterly', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('year', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('board', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='objectives', to='portfolio.board')),
            ],
            options={
                'ordering': ['-year', '-quarterly', 'text'],
            },
        ),
        migrations.CreateModel(
            name='KeyResultValue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('month', models.PositiveSmallIntegerField(blank=True, default=1)),
                ('value1', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('value2', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('value3', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('value4', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('final', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('kr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='values', to='portfolio.board')),
            ],
            options={
                'ordering': ['month'],
            },
        ),
        migrations.CreateModel(
            name='KeyResults',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('acronym', models.CharField(blank=True, max_length=6, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('objective', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='results', to='portfolio.board')),
            ],
            options={
                'ordering': ['acronym'],
            },
        ),
    ]