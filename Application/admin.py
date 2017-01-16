from django.contrib import admin
from Application.models import Feed,Item,UserProfile

# Register your models here.
admin.site.register(Feed)
admin.site.register(Item)
admin.site.register(UserProfile)