from django.contrib import admin

from .models import Color
from .models import Note
from .models import Tag

admin.site.register(Color)
admin.site.register(Tag)
admin.site.register(Note)