from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = 'Книжка Рецептів'
    verbose_name_plural = 'Книжка Рецептів'
