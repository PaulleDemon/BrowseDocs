# Generated by Django 4.2.6 on 2023-11-27 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docsapp', '0011_project_authors_alter_sponsor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='docpage',
            name='views',
            field=models.BigIntegerField(default=0),
        ),
    ]
