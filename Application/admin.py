from django.contrib import admin
from Application.models import Feed, Item, UserProfile, Section, Keyword, Status, Comment

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Section)
admin.site.register(Feed)
admin.site.register(Item)
admin.site.register(Status)
admin.site.register(Keyword)
admin.site.register(Comment)
