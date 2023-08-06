from typing import Any


def dget(structure: Any, *args, default: Any = None):
    for key in args:
        try:
            structure = structure[key]
        except:
            return default

    return structure
