from qronos_django.models import QRonosImportLog
from qronos_django.settings import QRONOS_LOGGING, QRONOS_ID_LOGGING, QRONOS_DATA_LOGGING
from qronos_django.tasks import process_import
from qronos import QRonosError


def tracker_import(tracker_id, unique_columns, can_add_item, can_delete_item, data):
    import_type = QRonosImportLog.QRonosImportType.TRACKER
    if QRONOS_LOGGING:
        import_log = QRonosImportLog.objects.create(
            import_type=import_type,
            id_log=f"Tracker ID: {tracker_id}, Can Add?: {can_add_item}, Can Delete?: {can_delete_item}" if QRONOS_ID_LOGGING else "LOGGING DISABLED",
            data_log=f"Unique Columns:\n{unique_columns}\n\nData:\n{data}" if QRONOS_DATA_LOGGING else "LOGGING DISABLED",
        )
        import_log_id = import_log.id
    else:
        import_log = None
        import_log_id = None
    process_import.delay(import_log_id, import_type, tracker_id, unique_columns, can_add_item, can_delete_item, data)
    return import_log


def stage_import(stage_id=None, tracker_stage_id=None, data=None):
    if stage_id:
        import_type = QRonosImportLog.QRonosImportType.STAGE
        id_log = f"Stage ID: {stage_id}" if QRONOS_ID_LOGGING else "LOGGING DISABLED",
    elif tracker_stage_id:
        import_type = QRonosImportLog.QRonosImportType.TRACKER_STAGE
        id_log = f"TrackerStage ID: {tracker_stage_id}" if QRONOS_ID_LOGGING else "LOGGING DISABLED",
    elif stage_id and tracker_stage_id:
        raise QRonosError("You can't provide both a stage_id and a tracker_stage_id")
    else:
        raise QRonosError("Provide either a stage_id or a tracker_stage_id")
    
    if QRONOS_LOGGING:
        import_log = QRonosImportLog.objects.create(
            import_type=import_type,
            id_log=id_log,
            data_log=f"Data:\n{data}" if QRONOS_DATA_LOGGING else "LOGGING DISABLED",
        )
        import_log_id = import_log.id
    else:
        import_log = None
        import_log_id = None
    process_import.delay(
        import_log_id,
        import_type,
        stage_id=stage_id,
        tracker_stage_id=tracker_stage_id,
        data=data
    )
    return import_log


def delete_items(tracker_id, data):
    import_type = QRonosImportLog.QRonosImportType.DELETE
    if QRONOS_LOGGING:
        import_log = QRonosImportLog.objects.create(
            import_type=import_type,
            id_log=f"Tracker ID: {tracker_id}" if QRONOS_ID_LOGGING else "LOGGING DISABLED",
            data_log=f"Data:\n{data}" if QRONOS_DATA_LOGGING else "LOGGING DISABLED",
        )
        import_log_id = import_log.id
    else:
        import_log = None
        import_log_id = None
    process_import.delay(import_log_id, import_type, tracker_id, data)
    return import_log
