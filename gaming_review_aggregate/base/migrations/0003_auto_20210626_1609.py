# Generated by Django 3.2 on 2021-06-26 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='promedio',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='review',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='game',
            name='plataforma',
            field=models.CharField(default='PC', max_length=150),
        ),
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.TextField(blank=True, max_length=2000),
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.game')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.game')),
            ],
        ),
        migrations.CreateModel(
            name='Friend_Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]