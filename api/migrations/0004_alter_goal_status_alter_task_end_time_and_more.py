# Generated by Django 5.0.1 on 2024-05-31 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_decription_goal_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='status',
            field=models.TextField(default='Pending'),
        ),
        migrations.AlterField(
            model_name='task',
            name='end_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.TextField(default='Pending'),
        ),
    ]
