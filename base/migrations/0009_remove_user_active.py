# Generated by Django 4.0 on 2022-05-29 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_course_courseid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='active',
        ),
    ]
