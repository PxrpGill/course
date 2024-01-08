# Generated by Django 4.2 on 2023-12-23 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_rating_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('average_rating',), 'verbose_name': 'инструмент', 'verbose_name_plural': 'Инструменты'},
        ),
        migrations.AddField(
            model_name='product',
            name='average_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='Рейтинг'),
        ),
    ]