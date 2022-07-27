from django.contrib import admin
from .models import Pet, Photo, Member


# Register your models here.
admin.site.register(Pet)
admin.site.register(Photo)
admin.site.register(Member)

class PetAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
