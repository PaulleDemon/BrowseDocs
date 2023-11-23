# Generated by Django 4.2.6 on 2023-11-23 12:20

from django.db import migrations, models
import django.db.models.deletion
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('docsapp', '0006_alter_project_unique_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=10)),
                ('lang', models.PositiveSmallIntegerField(choices=[(0, 'English'), (1, 'French'), (2, 'German'), (3, 'Russian')], default=0)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docsapp.project')),
            ],
        ),
        migrations.CreateModel(
            name='DocPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('page_url', models.CharField(max_length=250)),
                ('body', django_quill.fields.QuillField(blank=True, null=True)),
                ('documentation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docsapp.documentation')),
            ],
        ),
    ]
