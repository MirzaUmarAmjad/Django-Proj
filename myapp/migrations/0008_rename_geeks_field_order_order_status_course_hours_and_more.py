# Generated by Django 4.0.4 on 2022-05-29 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_student_options_alter_student_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='geeks_field',
            new_name='order_status',
        ),
        migrations.AddField(
            model_name='course',
            name='hours',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]