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


class FieldLinkAdmin(admin.ModelAdmin):

    exclude = []
    list_display = (
        'pk', 'field', 'subfield', 'sequence', 
        'text_before', 'text_after',
    )
    search_fields = ['field__name']


class CustomFieldAdmin(admin.ModelAdmin):

    exclude = []
    list_display = (
        'pk', 'field__name', 'rule__name',
        # 'priority'
    )
    # list_display_links = ['field']
    search_fields = ['field__name', 'rule__name']
    # list_filter = ['is_required', 'is_unique']
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
admin.site.register(Rule, GroupFieldAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(RuleSet, CustomFieldAdmin)
admin.site.register(Obj, CustomServiceAdmin)
admin.site.register(FieldLink, FieldLinkAdmin)
