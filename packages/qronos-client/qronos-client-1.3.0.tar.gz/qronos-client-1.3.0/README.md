# qronos-client
Python client for QRonos

## Installation

This package can be installed via pip:

```
pip install qronos-client
```

## Example Usage

### Authentication

```python
from qronos import QRonosClient

# Create client and login
qronos = QRonosClient(host='dev.qronos.xyz')
token, expiry = qronos.login(username='Quentin', password='Rogers')

# Alternatively, if you already have a token
qronos = QRonosClient(host='dev.qronos.xyz', token='ABCDEFGHIJKLMN')

# Logout
qronos.logout(all_tokens=True)
```

### Tracker (Item) Data Import

```python
# Import Tracker (Item) Data
job_id = qronos.tracker_import(
    tracker_id=24,
    unique_columns=["Part Number", "Weight"], 
    can_add_item=True,
    can_delete_item=False,
    data=[{"Part Number": "A1", "Weight": 5}, {"Part Number": "A2", "Weight": 8}],
)
```

### Stage Data Import

```python
# Import Stage Data
job_id = qronos.stage_import(
    stage_id=2,
    data=[{"Part Number": "A1", "leadtime": 5}, {"Part Number": "A2", "actual": "2020-10-26"}],
)
```

### Stage Data Import by Tracker Stage

```python
# Import Stage Data
job_id = qronos.stage_import(
    tracker_stage_id=2,
    data=[{"Part Number": "A1", "leadtime": 5}, {"Part Number": "A2", "actual": "2020-10-26"}],
)
```

### Import Status

```python
# Check Status of an Import
status = qronos.import_status(job_id=job_id)
```

### Delete Items
```python
# Delete Items
job_id = qronos.delete_items(
    tracker_id=2, 
    data=["A", "B"],
)
```

### Get Item Attribute Data

- At minimum you must request a `tracker` or a `unique_key`/`unique_keys`
- You cannot request both a `unique_key` and `unique_keys`

```python
# Get Item Attribute Data by tracker 
item_data = qronos.get_item_attributes(
    tracker=3,
    show_non_mastered=False,
    show_mastered=True,
)

# Get Item Attribute Data by unique keys
item_data = qronos.get_item_attributes(
    unique_keys=["800000689", "800000726", "800000727"],
    show_non_mastered=True,
    show_mastered=True,
)

# Get Item Attribute Data by single unique key
item_data = qronos.get_item_attributes(
    unique_key="800000689",
    show_non_mastered=False,
    show_mastered=True,
)

# Get Item Attribute Data by single unique key for only a single tracker
item_data = qronos.get_item_attributes(
    unique_key="800000689",
    tracker=4,
    show_non_mastered=False,
    show_mastered=True,
)
```

### Get Item Stage Data

- At minimum you must request a `tracker` or a `unique_key`/`unique_keys`
- You cannot request both a `unique_key` and `unique_keys`
- You cannot request both a `stage` and `stages`
- You cannot request both a `tracker_stage` and `tracker_stages`
- You cannot request a combinations of `stage` and `tracker_stage` fields

```python
# Get Item Stage Data for a tracker 
stage_data = qronos.get_item_stages(tracker=3)

# Get Item Stage Data by unique keys
stage_data = qronos.get_item_stages(unique_keys=["800000689", "800000726", "800000727"])

# Get Item Stage Data by single unique key but only for a single stage
stage_data = qronos.get_item_stages(
    unique_key="800000689",
    stage=54,
)

# Get Item Stage Data by single unique key but only for a single tracker stage
stage_data = qronos.get_item_stages(
    unique_key="800000689",
    tracker_stage=12,
)

# Get Item Stage Data for a list of stages on a certain tracker
stage_data = qronos.get_item_stages(
    tracker=4,
    stages=[54, 55, 56],
)

# Get Item Stage Data for a list of tracker stages on a certain tracker
stage_data = qronos.get_item_stages(
    tracker=4,
    tracker_stages=[12, 13, 14],
)
```

## Testing

Please speak with a QRonos Demo Site Admin for credentials in order to run the tests.
