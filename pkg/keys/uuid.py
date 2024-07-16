import os
import uuid
from threading import Lock

current_id = 0
mutex = Lock()

def generate_uuid() -> str:
    global current_id
    if os.getenv("DETERMINISTIC_IDS") == "true":
        with mutex:
            current_id += 1
            return str(current_id)
    return str(uuid.uuid4())