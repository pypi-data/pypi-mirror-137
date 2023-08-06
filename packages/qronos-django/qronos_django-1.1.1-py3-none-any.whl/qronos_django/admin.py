from django.contrib import admin, messages

from qronos_django.models import QRonosImportLog
from qronos_django.tasks import update_qronos_log_status


class QRonosImportLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'job_id', 'sent', 'status', 'status_updated']
    actions = ["update_status"]

    def update_status(self, request, queryset):
        update_qronos_log_status.delay([qi.id for qi in queryset.exclude(job_id=None)])
        self.message_user(request, "Statuses sent for update, please refresh shortly.", messages.SUCCESS)

    update_status.short_description = "Update Import Status"


admin.site.register(QRonosImportLog, QRonosImportLogAdmin)
