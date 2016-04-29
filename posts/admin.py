from django.contrib import admin

# Register your models here.
from .models import *
from .forms import admission_form






admin.site.register(admission)
admin.site.register(Tag)
admin.site.register(placement)
# admin.site.register(admviews)
