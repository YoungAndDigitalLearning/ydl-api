from django.contrib import admin
from quiz import models as m

# Register your models here.
admin.site.register(m.Test)
admin.site.register(m.Task)
admin.site.register(m.Answer)