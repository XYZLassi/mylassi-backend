__all__ = ['encode_cursor', 'decode_cursor']

import base64
import json
from typing import Optional


def encode_cursor(cursor: int) -> str:
    cursor_info = {
        'cursor_id': cursor
    }

    cursor_json = json.dumps(cursor_info)
    cursor = base64.b64encode(cursor_json.encode()).decode()
    return cursor


def decode_cursor(cursor: str) -> Optional[int]:
    try:

        cursor_json = base64.b64decode(cursor.encode()).decode()
        cursor_info: dict = json.loads(cursor_json)

        return cursor_info.get('cursor_id', None)

    except Exception as ex:
        return None
