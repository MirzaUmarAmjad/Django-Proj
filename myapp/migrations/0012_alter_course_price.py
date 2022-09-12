# Generated by Django 4.0.4 on 2022-08-05 14:14

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_course_interested_course_stages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[myapp.models.validate_price]),
        ),
    ]