# Generated by Django 2.2 on 2019-05-14 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_paper_n_citation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='reference',
        ),
        migrations.AddField(
            model_name='paper',
            name='recommend',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='search.Paper'),
        ),
    ]