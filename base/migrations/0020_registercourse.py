# Generated by Django 4.0 on 2022-06-12 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_auto_20220612_1910'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignedLect', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.assignlecturer')),
                ('user', models.ForeignKey(limit_choices_to={'student': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.user')),
            ],
        ),
    ]
