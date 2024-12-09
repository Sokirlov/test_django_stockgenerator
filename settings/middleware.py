from django.utils.deprecation import MiddlewareMixin
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.apps import apps


class AuditMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return
        request.current_user = request.user
        models = apps.get_models()
        for model in models:
            if hasattr(model, 'create_by') and hasattr(model, 'update_by'):
                @receiver(pre_save, sender=model)
                def set_audit_fields(sender, instance, **kwargs):
                    if not instance.pk:
                        instance.create_by = request.current_user
                    instance.update_by = request.current_user
