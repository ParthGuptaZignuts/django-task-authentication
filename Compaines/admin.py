from django.contrib import admin
from .models import Company , Department , Employee , Address , Project , Task

admin.site.register([Company , Department , Employee , Address , Project , Task])
