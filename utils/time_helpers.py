from datetime import datetime
import pytz #python timezone 替换时区


def utc_now():
    return datetime.now().replace(tzinfo=pytz.utc)