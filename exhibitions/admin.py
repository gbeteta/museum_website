from django.contrib import admin
from .models import *

admin.site.register(Gallery)
admin.site.register(Exhibition)
admin.site.register(Staff)

admin.site.register(Artifact)
admin.site.register(Organism)
admin.site.register(Fossil)
admin.site.register(Artwork)