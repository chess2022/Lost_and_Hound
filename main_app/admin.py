from django.contrib import admin
from .models import Pet, Photo


# Register your models here.
admin.site.register(Pet)
admin.site.register(Photo)

class PetAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
