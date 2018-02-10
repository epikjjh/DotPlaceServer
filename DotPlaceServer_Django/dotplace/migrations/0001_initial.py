# Generated by Django 2.0.1 on 2018-01-24 14:13

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
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageInArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/%Y/%m/%d')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dotplace.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('type', models.IntegerField()),
                ('duration', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.CharField(max_length=10)),
                ('gender', models.CharField(max_length=10)),
                ('nation', models.CharField(max_length=30)),
                ('profile_image', models.ImageField(upload_to='profiles/%Y/%m/%d')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('owner_index', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dotplace.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='position',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dotplace.Trip'),
        ),
        migrations.AddField(
            model_name='article',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dotplace.Position'),
        ),
    ]