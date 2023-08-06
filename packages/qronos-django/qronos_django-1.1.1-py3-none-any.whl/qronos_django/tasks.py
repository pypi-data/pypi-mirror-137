from celery import shared_task
from qronos import QRonosError

from qronos_django.connection import get_qronos_client
from qronos_django.models import QRonosImportLog
from qronos_django.settings import QRONOS_LOGGING


@shared_task
def process_import(import_log_id, import_type, *import_args, **import_kwargs):
    try:
        qronos = get_qronos_client()
        if import_type == QRonosImportLog.QRonosImportType.TRACKER:
            job_id = qronos.tracker_import(*import_args)
        elif import_type == QRonosImportLog.QRonosImportType.STAGE:
            job_id = qronos.stage_import(**import_kwargs)
        elif import_type == QRonosImportLog.QRonosImportType.TRACKER_STAGE:
            job_id = qronos.stage_import(**import_kwargs)
        elif import_type == QRonosImportLog.QRonosImportType.DELETE:
            job_id = qronos.delete_items(*import_args)
        else:
            raise QRonosError("Invalid Import Type")
    except QRonosError as err:
        qronos_log_data = {
            "job_id": None,
            "error_log": repr(err),
            "status": "FAIL",
        }
    else:
        qronos_log_data = {
            "job_id": job_id,
            "status": "UNKNOWN",
            "error_log": "",
        }
    if QRONOS_LOGGING:
        QRonosImportLog.objects.filter(id=import_log_id).update(**qronos_log_data)


@shared_task
def update_qronos_log_status(log_ids):
    qronos = get_qronos_client()
    for import_log in QRonosImportLog.objects.filter(id__in=log_ids).exclude(job_id=None):
        import_log.update_import_status(qronos)
