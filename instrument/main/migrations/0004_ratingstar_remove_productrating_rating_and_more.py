# Generated by Django 4.2 on 2023-12-22 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_productrating'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingStar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=0, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'звезда рейтинга',
                'verbose_name_plural': 'Звезды рейтинга',
                'ordering': ('-value',),
            },
        ),
        migrations.RemoveField(
            model_name='productrating',
            name='rating',
        ),
        migrations.AddField(
            model_name='productrating',
            name='star',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='main.ratingstar', verbose_name='Звезда'),
        ),
    ]
