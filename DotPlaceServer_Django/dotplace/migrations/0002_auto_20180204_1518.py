# Generated by Django 2.0.1 on 2018-02-04 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dotplace', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(null=True, upload_to='profiles/%Y/%m/%d'),
        ),
    ]