from django.contrib import admin

# Register your models here.

from files.models import *

admin.site.register(FileModel)
admin.site.register(FileHistoryModel)
admin.site.register(User)