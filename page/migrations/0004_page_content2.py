# Generated by Django 3.2.5 on 2021-08-20 11:51

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0003_remove_page_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='content2',
            field=ckeditor.fields.RichTextField(default=''),
        ),
    ]
