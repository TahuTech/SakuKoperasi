from django.contrib import admin
from .models import Member

admin.site.site_header = 'SakuKoperasi Administration'
admin.site.site_title = 'SakuKoperasi Admin'
admin.site.index_title = 'Dashboard Admin'

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id_member', 'name', 'id_week', 'id_month', 'phone_number')
    search_fields = ('id_member', 'name', 'phone_number')
