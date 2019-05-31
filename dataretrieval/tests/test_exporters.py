import os
import unittest

import exporters


class TestExporters(unittest.TestCase):
    def test_get_file_from_data_world(self):
        api_key = exporters.get_api_key()
        response = exporters.get_file_from_data_world('incidents', api_key)

        expectation = 200
        result = response.status_code

        self.assertEqual(expectation, result)

        response = exporters.get_file_from_data_world('fizzbop', api_key)

        expectation = 400
        result = response.status_code

        self.assertEqual(expectation, result)


if __name__ == '__main__':
    unittest.main()
