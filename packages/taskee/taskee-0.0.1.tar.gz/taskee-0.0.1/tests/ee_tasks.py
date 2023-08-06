COMPLETED_TASK = {
    "state": "COMPLETED",
    "description": "completed_task",
    "creation_timestamp_ms": 1641020000000,
    "update_timestamp_ms": 1641020000000 + 200000,
    "start_timestamp_ms": 1641020000000 + 100000,
    "task_type": "EXPORT_IMAGE",
    "destination_uris": ["https://drive.google.com/", "https://drive.google.com/"],
    "attempt": 1,
    "id": "id1",
    "name": "projects/earthengine-legacy/operations/ZSPQGTK2WGTEZJ3EFJWECCO3",
}

FAILED_TASK = {
    "state": "FAILED",
    "description": "failed_task",
    "creation_timestamp_ms": 1641020000000,
    "update_timestamp_ms": 1641020000000 + 20000,
    "start_timestamp_ms": 1641020000000 + 10000,
    "task_type": "EXPORT_IMAGE",
    "attempt": 1,
    "error_message": (
        "Export too large: specified 288009084 pixels (max: 1). Specify higher"
        " maxPixels value if you intend to export a large area."
    ),
    "id": "id2",
    "name": "projects/earthengine-legacy/operations/ZSPQGTK2WGTEZJ3EFJWECCO3",
}

CANCELLED_TASK = {
    "state": "CANCELLED",
    "description": "cancelled_task",
    "creation_timestamp_ms": 1641014000000,
    "update_timestamp_ms": 1641014000000 + 20000,
    "start_timestamp_ms": 1641014000000 + 10000,
    "task_type": "EXPORT_IMAGE",
    "attempt": 1,
    "error_message": "Cancelled.",
    "id": "id3",
    "name": "projects/earthengine-legacy/operations/ZSPQGTK2WGTEZJ3EFJWECCO3",
}

READY_TASK = {
    "state": "READY",
    "description": "ready_task",
    "creation_timestamp_ms": 1641028000000,
    "update_timestamp_ms": 1641028000000 + 5000,
    "start_timestamp_ms": 0,
    "task_type": "EXPORT_IMAGE",
    "id": "id4",
    "name": "projects/earthengine-legacy/operations/ZSPQGTK2WGTEZJ3EFJWECCO3",
}

RUNNING_TASK = {
    "state": "RUNNING",
    "description": "running_task",
    "creation_timestamp_ms": 1641030000000,
    "update_timestamp_ms": 1641030000000 + 20000,
    "start_timestamp_ms": 1641030000000 + 10000,
    "task_type": "EXPORT_IMAGE",
    "attempt": 1,
    "id": "id5",
    "name": "projects/earthengine-legacy/operations/ZSPQGTK2WGTEZJ3EFJWECCO3",
}

CANCEL_REQUESTED_TASK = {
    "state": "CANCEL_REQUESTED",
    "description": "cancel_requested_task",
    "creation_timestamp_ms": 1642990972694,
    "update_timestamp_ms": 1642990988770,
    "start_timestamp_ms": 1642990976014,
    "task_type": "EXPORT_IMAGE",
    "attempt": 1,
    "id": "BXGCHV6SSN3YOUUCR7XUWS34",
    "name": "projects/earthengine-legacy/operations/BXGCHV6SSN3YOUUCR7XUWS34",
}
