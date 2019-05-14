from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	list_display = ('username','email','is_admin','pass_for_api')
	list_filter = ('is_admin',)

	fieldsets = (
			(None, {'fields': ('username','email','password', 'pass_for_api')}),
			('Permissions', {'fields': ('is_admin',)})
		)
	search_fields = ('username','email')
	ordering = ('username','email')

	filter_horizontal = ()



admin.site.unregister(Group)