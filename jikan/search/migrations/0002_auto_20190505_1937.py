# Generated by Django 2.2 on 2019-05-05 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='abstract',
            field=models.CharField(max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='paper',
            name='authors',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='paper',
            name='reference',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='search.Paper'),
        ),
        migrations.AlterField(
            model_name='paper',
            name='venue',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='paper',
            name='year',
            field=models.IntegerField(null=True),
        ),
    ]
