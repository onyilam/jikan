# Generated by Django 2.2 on 2019-05-09 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_auto_20190508_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='n_citation',
            field=models.IntegerField(null=True),
        ),
    ]
