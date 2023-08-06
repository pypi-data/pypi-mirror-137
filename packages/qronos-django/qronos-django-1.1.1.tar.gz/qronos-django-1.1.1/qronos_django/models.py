from django.db import models
from django.utils import timezone
from qronos import QRonosError

from qronos_django.connection import get_qronos_client


class QRonosImportLog(models.Model):

    class QRonosImportType(models.TextChoices):
        TRACKER = "Tracker", "Tracker"
        STAGE = "Stage", "Stage"
        TRACKER_STAGE = "TrackerStage", "TrackerStage"
        DELETE = "Delete", "Delete"

    import_type = models.CharField(max_length=20, choices=QRonosImportType.choices)
    job_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, default="UNKNOWN")
    status_updated = models.DateTimeField(blank=True, null=True)
    id_log = models.TextField(blank=True)
    data_log = models.TextField(blank=True)
    error_log = models.TextField(blank=True)
    sent = models.DateTimeField(auto_now_add=True)

    def update_import_status(self, qronos=None):
        if not qronos:
            qronos = get_qronos_client()
        try:
            status = qronos.import_status(self.job_id)
        except QRonosError:
            status = "UNKNOWN"
        finally:
            self.status = status
            self.status_updated = timezone.now()
            self.save()
        return status

    class Meta:
        verbose_name = "QRonos Import Log"
        verbose_name_plural = "QRonos Import Logs"

    def __str__(self):
        return f"QRonos Import {self.id} (TP: {self.job_id or '-'})"
