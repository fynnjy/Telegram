# Generated by Django 4.1.2 on 2022-10-30 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=20, null=True, verbose_name='Назва')),
                ('photo', models.ImageField(null=True, upload_to='images/', verbose_name='Зображення')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Опис')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепти',
                'db_table': 'recipes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=30, null=True, verbose_name='Нікнейм')),
                ('input_name', models.CharField(blank=True, max_length=15, null=True, verbose_name="Введене ім'я")),
                ('gender', models.CharField(blank=True, max_length=15, null=True, verbose_name='Стать')),
                ('first_name', models.CharField(blank=True, max_length=25, null=True, verbose_name="Ім'я")),
                ('last_name', models.CharField(blank=True, max_length=35, null=True, verbose_name='Прізвище')),
                ('registration_date', models.DateField(blank=True, max_length=30, null=True, verbose_name='Дата реєстрації')),
            ],
            options={
                'verbose_name': 'Користувач',
                'verbose_name_plural': 'Користувачі',
                'db_table': 'users',
                'managed': False,
            },
        ),
    ]