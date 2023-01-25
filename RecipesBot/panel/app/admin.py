from .models import Users, Recipes
from django.contrib import admin


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_filter = ("gender",)
    list_display = ("first_name", "last_name", "username", "id",
                    "input_name", "gender", "registration_date")
    search_fields = ["first_name", "last_name", "username", "id",
                     "input_name", "gender", "registration_date"]


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ["title"]


admin.site.site_title = 'Книжка Рецептів'
admin.site.site_header = 'Книжка Рецептів'
