# Generated by Django 2.0.1 on 2018-03-18 04:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('numofdots', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DotPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.FloatField(default=0.0)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('is_dot', models.BooleanField()),
                ('pin', models.BooleanField(default=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schimcalculator.Area')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schim', models.IntegerField(default=0)),
                ('newsfeed', models.IntegerField(default=0)),
                ('alpha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alpha', to=settings.AUTH_USER_MODEL)),
                ('omega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='omega', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]