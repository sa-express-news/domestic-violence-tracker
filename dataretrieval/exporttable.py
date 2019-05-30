class ExportTable():
    __init__(self, schema):
        self.schema = schema
        self._data = []

    def _field_exists(self, key):
        return key in schema

    def _validate_and_prune(self, hash):
        for key, val in hash.items():
            if not self._field_exists(key):
                raise Exception(f'Hash is missing field: {key}')

    def add_hash(self, hash):
        if self._is_valid(hash):
            self._data.append(hash)
