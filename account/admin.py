from django.contrib import admin

from account.models import Salon, User

# Register your models here.
admin.site.register(User)
admin.site.register(Salon)
