from django.apps import AppConfig
from django.db.models.signals import post_migrate

class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"

    def ready(self):
        from django.contrib.auth.models import Group
        from django.dispatch import receiver

        @receiver(post_migrate)
        def create_default_groups(sender, **kwargs):
            roles = ['default user', 'student', 'teacher', 'fin_support', 'tech_support']
            for role in roles:
                Group.objects.get_or_create(name=role)
