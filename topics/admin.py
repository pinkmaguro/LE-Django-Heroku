from django.contrib import admin
from topics.models import Topic, Entry

admin.site.register(Topic)
admin.site.register(Entry)