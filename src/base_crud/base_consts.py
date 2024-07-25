from enum import Enum


class Method(Enum):
    get = "get"
    get_all = "get_all"
    create = "create"
    delete = "delete"
    update = "update"
    partial_update = "partial_update"


METHOD_WRAPPER = {
    Method.get: "get",
    Method.get_all: "get",
    Method.create: "post",
    Method.delete: "delete",
    Method.update: "put",
    Method.partial_update: "patch"
}

FILE_METHODS = {Method.get, Method.create, Method.get_all, Method.delete}
DEFAULT_METHODS = {Method.get, Method.create, Method.get_all, Method.update, Method.partial_update, Method.delete}
SINGLE_METHODS = {Method.get, Method.delete, Method.update, Method.partial_update}
