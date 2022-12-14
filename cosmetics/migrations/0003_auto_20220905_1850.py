# Generated by Django 3.2.10 on 2022-09-05 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmetics', '0002_auto_20220902_1052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['id'], 'verbose_name': 'Фотография товара', 'verbose_name_plural': '4. Фотографии товаров'},
        ),
        migrations.AlterField(
            model_name='product',
            name='skin_type',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Тип кожи'),
        ),
        migrations.AlterField(
            model_name='product',
            name='skin_type_ru',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Тип кожи'),
        ),
        migrations.AlterField(
            model_name='product',
            name='skin_type_uk',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Тип кожи'),
        ),
    ]
