from django.contrib import admin
from .models import NewsFeedItem,Like

admin.site.register(NewsFeedItem)
admin.site.register(Like)



admin.site.site_header = "Social Media ";

