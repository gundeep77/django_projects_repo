# Generated by Django 3.1.3 on 2020-11-24 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newloan',
            name='fname',
            field=models.CharField(default='', max_length=50),
        ),
    ]
