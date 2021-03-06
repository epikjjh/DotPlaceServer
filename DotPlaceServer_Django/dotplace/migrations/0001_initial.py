# Generated by Django 2.0.1 on 2018-03-03 05:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import dotplace.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_name', models.CharField(max_length=20, unique=True)),
                ('phone_number', models.CharField(max_length=25, unique=True)),
                ('email', models.EmailField(max_length=25, unique=True)),
                ('birthday', models.CharField(max_length=10)),
                ('gender', models.CharField(max_length=10)),
                ('nation', models.CharField(max_length=30)),
                ('profile_image', models.ImageField(null=True, upload_to=dotplace.models.profile_image_path)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
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
                ('image', models.ImageField(upload_to=dotplace.models.article_image_path)),
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
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('owner_index', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
