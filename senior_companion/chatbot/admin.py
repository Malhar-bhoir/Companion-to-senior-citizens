from django.contrib import admin
from .models import LogicRule, UnansweredQuery

@admin.register(LogicRule)
class LogicRuleAdmin(admin.ModelAdmin):
    list_display = ('pattern', 'match_type', 'priority', 'response')
    ordering = ('-priority',)
    search_fields = ('pattern', 'response')

@admin.register(UnansweredQuery)
class UnansweredQueryAdmin(admin.ModelAdmin):
    list_display = ('query_text', 'user', 'timestamp', 'is_resolved')
    list_filter = ('is_resolved', 'timestamp')
    readonly_fields = ('timestamp',)
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
    mark_as_resolved.short_description = "Mark selected queries as resolved"