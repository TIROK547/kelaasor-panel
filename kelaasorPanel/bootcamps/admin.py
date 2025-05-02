from django.contrib import admin
from .models import BootCampCategory, BootCamp, BootCampParticipant, BootCampsJoinRequest

admin.site.register(BootCamp)
admin.site.register(BootCampCategory)
admin.site.register(BootCampParticipant)
admin.site.register(BootCampsJoinRequest)