# Generated by Django 2.2 on 2019-05-26 16:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0012_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preference',
            name='value',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(20)]),
        ),
    ]
