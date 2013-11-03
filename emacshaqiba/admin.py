from django.contrib import admin
from emacshaqiba.models import CodeTemplate, UserProfile, Dependency
from emacshaqiba.models import BundleTemplate

admin.site.register(CodeTemplate)
admin.site.register(UserProfile)
admin.site.register(Dependency)
admin.site.register(BundleTemplate)

