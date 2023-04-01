from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "hotelbooking.utils"

    def ready(self):
        from . import checks  # noqa
