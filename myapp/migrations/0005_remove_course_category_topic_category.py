# Generated by Django 4.0.4 on 2022-05-29 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_course_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='category',
        ),
        migrations.AddField(
            model_name='topic',
            name='category',
            field=models.CharField(default='', max_length=200),
        ),
    ]
