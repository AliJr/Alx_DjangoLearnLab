# Generated by Django 5.1.3 on 2024-12-07 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_customuser_profile_picture_alter_customuser_bio_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-published_date']},
        ),
    ]
