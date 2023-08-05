# Generated by Django 3.2.2 on 2021-12-07 10:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juntagrico_assignment_request', '0003_change_assignment_helptext'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentrequest',
            name='amount',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Wert'),
        ),
        migrations.AlterField(
            model_name='assignmentrequest',
            name='duration',
            field=models.DecimalField(decimal_places=2, default=4.0, max_digits=4, verbose_name='Dauer in Stunden'),
        ),
    ]
