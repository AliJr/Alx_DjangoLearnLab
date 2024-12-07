# Generated by Django 5.1.3 on 2024-12-07 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='posts', to='blog.tag'),
        ),
    ]
