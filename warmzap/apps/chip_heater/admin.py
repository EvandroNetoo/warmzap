from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from chip_heater.models import Chip, Message

admin.site.register(Chip)


class MessageResource(resources.ModelResource):
    class Meta:
        model = Message
        fields = ('message',)
        export_order = (
            'id',
            'message',
        )
        import_id_fields = ('message',)
        skip_unchanged = True
        report_skipped = False


@admin.register(Message)
class MessageAdmin(ImportExportModelAdmin):
    resource_class = MessageResource
    list_display = ['message']
