from io import BufferedRandom
import json
import os
from typing import *


class FileWriter:
    _h_data: BufferedRandom
    _h_index: BufferedRandom
    _index: Mapping[str, tuple[int, int]]
    _close: bool

    def __init__(self, path: str) -> None:
        self._index = {}
        self._close = False

        p_data = os.path.join(path, 'db.tpd')
        self._h_data = open(p_data, 'wb+')
        self._h_data.truncate()

        p_index = os.path.join(path, 'db.tpi')
        self._h_index = open(p_index, 'wb+')
        self._h_index.truncate()

    def __del__(self):
        self._index = None
        self._close = True

        if self._h_data:
            self._h_data.close()

        if self._h_index:
            self._h_index.close()

    def __enter__(self):
        if self._close:
            raise Exception('Already closed')
        return self

    def __exit__(self, type, value, trace):
        if not self._close:
            self.close(type != None)
            self._close = True

    def write(self, id: str, data: str, cache: int):
        if self._close:
            raise Exception('Already closed')

        if id in self._index:
            raise Exception('ID conflict: %s' % id)

        start = self._h_data.tell()
        self._h_data.write(str.encode(data))
        finish = self._h_data.tell()
        self._h_data.write(str.encode('\n'))
        self._index[id] = (start, finish-start, cache)

    def close(self, clear: bool = False):
        if self._close:
            raise Exception('Already closed')
        self._close = True

        if self._h_data:
            if clear:
                self._h_data.truncate()
            self._h_data.flush()

        if self._h_index:
            if clear:
                self._h_index.truncate()
            else:
                data = json.dumps(self._index)
                self._h_index.write(str.encode(data))
                self._h_index.flush()

        self._index = None


# class ResSet:
#     _id_set: set[str]
#     _res_list: list[Resource]

#     def __init__(self) -> None:
#         self._id_set = set([])
#         self._res_list = []

#     def add(self, res: Resource):
#         if res.res_id in self._id_set:
#             raise Exception('ID conflict: %s' % res.res_id)
#         self._id_set.add(res.res_id)
#         self._res_list.append(res)


# class ResDB:
#     _sets: dict[str, ResSet]

#     def __init__(self):
#         self._sets = {}

#     def __lshift__(self, res: Resource):
#         res.verify()
#         if res.T not in self._sets:
#             self._sets[res.T] = ResSet()
#         set = self._sets[res.T]
#         set.add(res)
#         return self

#     def to_string(self, ident: str = '  ') -> str:
#         list = []
#         for set in self._sets.values():
#             for res in set._res_list:
#                 list.append(res.serialize())
#         return json.dumps(list, indent=ident)

#     def write_to(self, path: str):
#         with FileWriter(path) as writer:
#             for set in self._sets.values():
#                 for res in set._res_list:
#                     data = json.dumps(res.serialize(), separators=(',', ':'))
#                     cache = res.cache == True and 1 or 0
#                     writer.write(res.res_id, data, cache)


# DB = ResDB()
