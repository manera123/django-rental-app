from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(NewAdvt)
admin.site.register(NewAdvtLocation)
admin.site.register(NewAdvtInformation)
admin.site.register(NewAdvtLastStep)
admin.site.register(NewAdvtImages)
admin.site.register(UserFavoriteAdvt)
admin.site.register(DocumentsCheckRequest)
admin.site.register(AdvtReservation)