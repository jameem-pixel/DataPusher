from django.contrib import admin
from .import models as server_models

admin.site.register(server_models.Account)
admin.site.register(server_models.Destination)
# Register your models here.
