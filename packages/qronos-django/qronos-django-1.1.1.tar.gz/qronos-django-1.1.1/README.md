# qronos-django
Django package for using the QRonos Python Client

## Installation

This package can be installed via pip:

```
pip install qronos-django
```

Add to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "qronos_django",
    ...
]
```

## Required Settings

### `QRONOS_HOST`
Default: `"dev.qronos.xyz"`

The URL host of the QRonos instance.

### `QRONOS_USER`
Default: `""`

The username with which to authenticate.

### `QRONOS_PASSWORD`
Default: `""`

The password with which to authenticate.

## Optional Settings

### `QRONOS_TOKEN_CACHE_KEY`
Default: `"QRONOS_TOKEN"`

The name of the cache key for Tokens

### `QRONOS_TOKEN_CACHE_FRACTION`
Default: `0.8`

What fraction of the total lifetime of tokens to cache.  Set to 0 to disable Token caching.

### `QRONOS_LOGGING`
Default: `True`

Create QRonosImportLog items in the Database to track the triggered QRonos Imports

### `QRONOS_ID_LOGGING`
Default: `False`

Store the tracker/stage ID's in the QRonosImportLog items

### `QRONOS_DATA_LOGGING`
Default: `False`

Store the data sent in the QRonosImportLog items

## Example Usage

```python
from qronos_django.imports import tracker_import, stage_import, delete_items
from qronos_django.tasks import update_qronos_log_status

# Import Tracker (Item) Data
# If QRONOS_LOGGING enabled then this will create a QRonosImportLog item and return it, otherwise returns None
import_log = tracker_import(
    tracker_id=24,
    unique_columns=["Part Number", "Weight"], 
    can_add_item=True,
    can_delete_item=False,
    data=[{"Part Number": "A1", "Weight": 5}, {"Part Number": "A2", "Weight": 8}],
)

# Import Stage Data
# If QRONOS_LOGGING enabled then this will create a QRonosImportLog item and return it, otherwise returns None
import_log = stage_import(
    stage_id=2,
    data=[{"Part Number": "A1", "leadtime": 5}, {"Part Number": "A2", "actual": "2020-10-26"}],
)

# Import Stage Data by Tracker Stage
# If QRONOS_LOGGING enabled then this will create a QRonosImportLog item and return it, otherwise returns None
import_log = stage_import(
    tracker_stage_id=2,
    data=[{"Part Number": "A1", "leadtime": 5}, {"Part Number": "A2", "actual": "2020-10-26"}],
)

# Delete Items
# If QRONOS_LOGGING enabled then this will create a QRonosImportLog item and return it, otherwise returns None
import_log = delete_items(
    tracker_id=2, 
    data=["A", "B"],
)

# Update (and return) status of a single QRonos Import Log.  Can pass optional qronos parameter if you already have a QRonosClient object.
status = import_log.update_import_status()

# (Async) Update Status of a set of QRonos Import Logs (note use QRonosImportLog ids, not job ids)
update_qronos_log_status.delay([125, 233])
```
