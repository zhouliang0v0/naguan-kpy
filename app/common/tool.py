import uuid


def get_event_request_id():
    return str(uuid.uuid5(uuid.uuid4(), 'event'))


def get_request_id():
    return str(uuid.uuid5(uuid.uuid4(), 'request'))


def get_task_request_id():
    return str(uuid.uuid5(uuid.uuid4(), 'task'))
