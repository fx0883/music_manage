from django.apps import AppConfig
from django.contrib import admin


class MusicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'music'

    def ready(self):
        from django.utils.module_loading import autodiscover_modules
        print("Starting admin class discovery...")
        autodiscover_modules('admin_classes', register_to=admin.site)
        print("Registered models:", admin.site._registry.keys())
