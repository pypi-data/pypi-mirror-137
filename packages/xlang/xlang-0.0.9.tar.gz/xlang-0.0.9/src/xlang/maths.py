# -*- coding: utf8 -*-
from xlang import logger

import string
import random

SHORT_NAME_SIZE = 6
ASCII_CHARACTER = string.ascii_letters + string.digits


def generate(length=SHORT_NAME_SIZE):
    return ''.join(random.sample(ASCII_CHARACTER, length))


def unique_file_name(file_name, length=SHORT_NAME_SIZE):
    return '%s.%s' % (generate(length), file_name[file_name.rfind('.') + 1:])


def to_bool(o) -> bool:
    return True if o in [True, 'True', 'true', 'yes', 'on', '1'] else to_int(o) > 0


def to_int(o, default: int = 0) -> int:
    v: int = default

    try:
        v = int(o)
    except Exception as e:
        logger.error(e)

    return v


def to_float(o, default: float = 0) -> float:
    v = default

    try:
        v = float(o)
    except Exception as e:
        logger.error(e)

    return v
