# Generated by Django 5.2.4 on 2025-07-25 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='meta_description',
            field=models.CharField(blank=True, help_text='Recommended: Max 160 characters for SEO', max_length=160),
        ),
        migrations.AddField(
            model_name='blog',
            name='seo_title',
            field=models.CharField(blank=True, help_text='Recommended: Max 60 characters', max_length=60),
        ),
    ]
