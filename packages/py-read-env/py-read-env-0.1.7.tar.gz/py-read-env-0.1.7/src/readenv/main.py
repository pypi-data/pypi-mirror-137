import os

from dotenv import dotenv_values


def hasKey(items_list, key):
    try:
        return items_list[key]
    except KeyError:
        # Key is not present
        return None


# TODO check Exception handling py
def hasKeyOsEnv(key):
    try:
        return os.getenv(key)
    except Exception as e:
        return None


class ReadPriority:
    FILE = 1
    OS = 2


class ReadEnv:
    path: str
    var_list_path: dict
    priority: ReadPriority

    def __init__(self, path='./', file='.env', var_list=None, priority=ReadPriority.FILE, debug=False):
        self.var_list = var_list
        self.path = path
        self.set_priority(priority)
        self.var_list_path = dotenv_values(os.path.join(path, file))
        for item in self.var_list_path:
            value = self.var_list_path[item]
            if value is not None:
                os.environ[item] = value

    def set_priority(self, priority):
        self.priority = priority

    def get(self, key):
        value_os = hasKeyOsEnv(key)
        value_file = None

        if hasKey(self.var_list_path, key):
            value_file = self.var_list_path[key]

        if self.priority == ReadPriority.OS:
            if value_os is not None:
                return value_os
            if value_file is not None:
                return value_file
        else:
            if value_file is not None:
                return value_file
            if value_os is not None:
                return value_os

        return None
