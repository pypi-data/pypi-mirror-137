from django.db import models
from django.contrib.auth import get_user_model
import pathlib
from .functions import (
    to_datetime
)
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger("sh")

DEFAULT_AUTH_FUNCTION_STR = open(
    pathlib.Path(__file__).parent.resolve() / "auth_function_default.py", "r"
).read()

class ShellSettings(models.Model):
    code_before = models.TextField(null=True)
    code_after = models.TextField(null=True)
    auth_function = models.TextField(null=True, default=DEFAULT_AUTH_FUNCTION_STR)

    def _evaluate_auth_function(self, request):
        if not self.auth_function:
            return request.user.is_superuser
        
        try:
            exec(self.auth_function)

            _locals = locals()
            if "is_valid_user" in _locals:
                return _locals["is_valid_user"](request)
            else:
                logger.error(f"No se encontró la función is_valid_user en locals()")
            
            return request.user.is_superuser

        except Exception as e:
            logger.error(str(e))
            return request.user.is_superuser
    
    def is_valid_request(self, request):
        if not self._evaluate_auth_function(request):
            raise Exception("El request es inválido, no cuenta con permisos para continuar")


class Command(models.Model):
    text = models.TextField(null=True)
    output = models.TextField(null=True)
    error = models.TextField(null=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    user = models.ForeignKey(get_user_model()(), related_name="sh_commands", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ("-id",)
    
    def to_dict(self):
        return {
            "id": self.pk,
            "output": self.output,
        }

    @classmethod
    def get_objects(cls, vars):
        q = vars.get("q","")
        desde = vars.get("desde")
        hasta = vars.get("hasta")
        objects = cls.objects.all()
       
        if q:
            objects = objects.filter(
                models.Q(text__icontains=q)
            )
        if desde:
            desde = to_datetime(desde, min=True)
            objects = objects.filter(start__gte=desde)
    
        if hasta:
            hasta = to_datetime(hasta, max=True)
            objects = objects.filter(start__lte=hasta)

        return objects

class SavedCommand(models.Model):
    user = models.ForeignKey(get_user_model()(), related_name="sh_saved_commands", on_delete=models.CASCADE)
    command = models.ForeignKey(Command, related_name="users", on_delete=models.PROTECT)
    description = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
