import json
from datetime import datetime
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


def get_iso_8601_date():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
