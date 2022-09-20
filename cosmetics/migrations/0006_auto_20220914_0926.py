# Generated by Django 3.2.10 on 2022-09-14 06:26

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmetics', '0005_alter_image_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhySkinBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=150, null=True, unique=True, verbose_name='Ссылка')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name="Содержание post'a")),
                ('published', models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='Просмотры')),
                ('status', models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=20)),
            ],
            options={
                'verbose_name': 'Публикация',
                'verbose_name_plural': 'Публикации блога',
                'ordering': ['-published'],
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name': 'Рубрика', 'verbose_name_plural': '5. Рубрики'},
        ),
    ]