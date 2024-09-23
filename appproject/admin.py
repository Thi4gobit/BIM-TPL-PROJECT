from django.contrib import admin 
from .models import *


class GroupFieldAdmin(admin.ModelAdmin):

    list_display = ('pk', 'name',)
    search_fields = ['name']


class FieldAdmin(admin.ModelAdmin):

    list_display = ('pk', 'name',)
    search_fields = ['name']


class ItemAdmin(admin.ModelAdmin):

    list_display = ('pk', 'item',)
    search_fields = ['item']


class FieldSelfRelationshipAdmin(admin.ModelAdmin):

    exclude = []
    list_display = (
        'pk', 'field', 'subfield', 'sequence', 
        'text_before', 'text_after',
    )
    search_fields = ['field__name']


class CustomFieldAdmin(admin.ModelAdmin):

    exclude = []
    list_display = (
        'pk', 'field__name', 'group__name', 'is_required', 'is_unique',
        'priority'
    )
    # list_display_links = ['field']
    search_fields = ['field__name', 'group__name']
    list_filter = ['is_required', 'is_unique']
    show_facets = admin.ShowFacets.ALWAYS


class CustomServiceAdmin(admin.ModelAdmin):

    exclude = []
    list_display = ('pk', 'item__item', 'field__field__name', 'value',)
    # list_display_links = ['field__field__name']
    search_fields = ['item__item', 'field__field__name']
    show_facets = admin.ShowFacets.ALWAYS


admin.site.site_header = ""
admin.site.site_title = "BIM-PROJECT"
admin.site.index_title = ""
admin.site.register(GroupField, GroupFieldAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(CustomField, CustomFieldAdmin)
admin.site.register(CustomService, CustomServiceAdmin)
admin.site.register(FieldSelfRelationship, FieldSelfRelationshipAdmin)
