from django.contrib import admin
from .models import MessageFeatures, Messages, Dialogue
# Register your models here.

admin.site.register([MessageFeatures, Messages])

admin.site.register([Dialogue])