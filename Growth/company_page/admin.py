from django.contrib import admin

# Register your models here.
from .models import Company, File, Photo

admin.site.register(Company)
admin.site.register(File)
admin.site.register(Photo)

