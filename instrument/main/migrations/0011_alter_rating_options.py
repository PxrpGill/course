# Generated by Django 4.2 on 2023-12-23 00:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_rating_options_rating_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'ordering': ('-created_at',), 'verbose_name': 'рейтинг', 'verbose_name_plural': 'Рейтинги'},
        ),
    ]