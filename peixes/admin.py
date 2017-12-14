from django.contrib import admin

from .models import Lote, Determinação, Tecido, Coletor, Projeto, Profile

# Register our Appointment model with the basic ModelAdmin
admin.site.register(Lote, admin.ModelAdmin)
admin.site.register(Determinação, admin.ModelAdmin)
admin.site.register(Tecido, admin.ModelAdmin)
admin.site.register(Coletor, admin.ModelAdmin)
admin.site.register(Projeto, admin.ModelAdmin)
admin.site.register(Profile, admin.ModelAdmin)
