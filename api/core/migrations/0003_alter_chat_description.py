# Generated by Django 4.1.7 on 2023-03-19 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='description',
            field=models.TextField(blank=True, default=None, max_length=255, null=True),
        ),
    ]