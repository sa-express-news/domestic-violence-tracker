from functools import reduce


class ExportModel():
    __init__(self, valid_fields):
        self._valid_fields = set(valid_fields)
        self._data = []

    def _is_valid(self, hash):
        return all(key in self._valid_fields for key in hash)

    def add_hash(self, hash):
        if self._is_valid(hash):
            self._data.append(hash)

    def merge_hashes(self, *argv):
        return reduce(lambda x, y: {**x, **y}, argv, {})
