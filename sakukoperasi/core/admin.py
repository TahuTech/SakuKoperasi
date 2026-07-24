from django.contrib import admin
from .models import Member, Savings, SavingsTransaction

admin.site.site_header = 'SakuKoperasi Administration'
admin.site.site_title = 'SakuKoperasi Admin'
admin.site.index_title = 'Dashboard Admin'

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id_member', 'name', 'id_week', 'id_month', 'phone_number')
    search_fields = ('id_member', 'name', 'phone_number')


class SavingsTransactionInline(admin.TabularInline):
    """Inline admin untuk SavingsTransaction di dalam Savings."""
    model = SavingsTransaction
    extra = 1
    fields = ('transaction_type', 'amount', 'transaction_date', 'notes', 'balance_before', 'balance_after', 'created_at')
    readonly_fields = ('balance_before', 'balance_after', 'created_at')
    ordering = ('-transaction_date', '-created_at')


@admin.register(Savings)
class SavingsAdmin(admin.ModelAdmin):
    """Admin untuk menampilkan dan manage tabungan anggota."""
    list_display = ('member', 'get_member_id', 'balance', 'updated_at')
    search_fields = ('member__id_member', 'member__name')
    readonly_fields = ('balance', 'created_at', 'updated_at')
    inlines = [SavingsTransactionInline]
    
    fieldsets = (
        ('Informasi Anggota', {
            'fields': ('member',),
        }),
        ('Saldo Tabungan', {
            'fields': ('balance', 'updated_at', 'created_at'),
            'description': 'Saldo otomatis diperbarui saat ada transaksi.',
        }),
    )
    
    def get_member_id(self, obj):
        return obj.member.id_member
    get_member_id.short_description = 'ID Anggota'
    
    def has_add_permission(self, request):
        """Savings dibuat otomatis saat Member dibuat, jadi tidak perlu add manual."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Hindari penghapusan akak tabungan."""
        return False


@admin.register(SavingsTransaction)
class SavingsTransactionAdmin(admin.ModelAdmin):
    """Admin untuk menampilkan dan membuat transaksi tabungan."""
    list_display = ('member_name', 'transaction_type', 'amount', 'balance_before', 'balance_after', 'transaction_date')
    list_filter = ('transaction_type', 'transaction_date', 'created_at')
    search_fields = ('savings__member__id_member', 'savings__member__name')
    readonly_fields = ('balance_before', 'balance_after', 'created_at')
    date_hierarchy = 'transaction_date'
    
    fieldsets = (
        ('Informasi Transaksi', {
            'fields': ('savings', 'transaction_type', 'transaction_date', 'amount'),
        }),
        ('Detail Saldo', {
            'fields': ('balance_before', 'balance_after'),
            'description': 'Otomatis dihitung saat transaksi disimpan.',
        }),
        ('Catatan', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    def member_name(self, obj):
        return f"{obj.savings.member.id_member} - {obj.savings.member.name}"
    member_name.short_description = 'Anggota'
    
    def get_queryset(self, request):
        """Optimize query dengan select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('savings__member')
