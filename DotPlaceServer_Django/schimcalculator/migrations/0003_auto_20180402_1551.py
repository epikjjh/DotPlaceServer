# Generated by Django 2.0.3 on 2018-04-02 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schimcalculator', '0002_auto_20180328_1629'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dotplace',
            options={'ordering': ['-ticket']},
        ),
        migrations.RemoveField(
            model_name='dotplace',
            name='pin',
        ),
    ]