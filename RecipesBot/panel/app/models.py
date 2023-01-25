from django.db import models


class Users(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    username = models.CharField("Нікнейм", blank=True, null=True, max_length=30)
    input_name = models.CharField("Введене ім'я", blank=True, null=True, max_length=15)
    gender = models.CharField("Стать", blank=True, null=True, max_length=15)
    first_name = models.CharField("Ім'я", blank=True, null=True, max_length=25)
    last_name = models.CharField("Прізвище", blank=True, null=True, max_length=35)
    registration_date = models.DateField("Дата реєстрації", blank=True, null=True, max_length=30)

    def __str__(self):
        return self.username

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'


class Recipes(models.Model):
    title = models.CharField("Назва", blank=True, null=True, max_length=20)
    photo = models.ImageField("Зображення", null=True, upload_to='images/')
    description = models.TextField("Опис", blank=True, null=True, max_length=1000)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепти'
