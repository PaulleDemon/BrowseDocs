# Generated by Django 4.2.6 on 2023-11-18 05:36

from django.db import migrations, models
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorial',
            name='text',
        ),
        migrations.AddField(
            model_name='tutorial',
            name='body',
            field=django_quill.fields.QuillField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='tag',
            field=models.CharField(max_length=150),
        ),
    ]
