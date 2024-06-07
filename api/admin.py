from django.contrib import admin
from .models import Todo, Goal, Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display=('user', 'uid', 'bio')
    
# Register your models here.
admin.site.register(Todo)
admin.site.register(Goal)
admin.site.register(Profile, ProfileAdmin)


