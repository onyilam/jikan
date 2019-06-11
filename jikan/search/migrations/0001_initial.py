# Generated by Django 2.2 on 2019-05-05 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('venue', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('abstract', models.CharField(max_length=10000)),
                ('authors', models.CharField(max_length=1000)),
                ('reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Paper')),
            ],
        ),
    ]
