# Generated by Django 4.0.4 on 2022-05-29 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_topic_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={},
        ),
        migrations.AlterModelTable(
            name='student',
            table='Students',
        ),
    ]
