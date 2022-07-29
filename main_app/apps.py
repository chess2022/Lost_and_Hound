from django.apps import AppConfig
# from django.db.models.signals import pre_save


class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'

    # def ready(self):
    #     # importing model classes
    #     from .models import Pet, Member, Photo  

    #     # registering signals with the model's string label
    #     pre_save.connect(receiver, sender=['main_app.Pet','main_app.Member','main_app.Photo'])

