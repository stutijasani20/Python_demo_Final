from django.contrib import admin

from .models import *

admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Company)
admin.site.register(Applicant)