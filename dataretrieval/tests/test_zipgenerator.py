import unittest
import io
import zipfile

from zipgenerator import ZipGenerator


class TestZipGenerator(unittest.TestCase):
    def test__get_incidents_idx(self):
        """Test obtaining incidents index"""
        zips = [
            zipfile.ZipInfo(filename='one'),
            zipfile.ZipInfo(filename='two'),
            zipfile.ZipInfo(filename='TX/NIBRS_incident.csv'),
            zipfile.ZipInfo(filename='three'),
            zipfile.ZipInfo(filename='four'),
        ]

        zip_generator = ZipGenerator('TX', 2017)
        
        expected = 2
        result = zip_generator._get_incidents_idx(zips)

        self.assertEqual(result, expected)

    def test__build_url(self):
        """build an fbi download url"""
        zip_generator = ZipGenerator('USA', 1847)
        expected = 'http://s3-us-gov-west-1.amazonaws.com/cg-d4b776d0-d898-4153-90c8-8336f86bdfec/1847/USA-1847.zip'
        result = zip_generator._url

        self.assertEqual(result, expected)

    def test__move_incidents_to_end_of_list(self):
        """Test moving list item to end of list"""
        infolist_one = [
            zipfile.ZipInfo(filename='one'),
            zipfile.ZipInfo(filename='FL/NIBRS_incident.csv'),
            zipfile.ZipInfo(filename='two'),
        ]

        infolist_two = [
            zipfile.ZipInfo(filename='one'),
            zipfile.ZipInfo(filename='FL/NIBRS_incident.csv'),
        ]

        zip_generator = ZipGenerator('FL', 2010)
        
        zip_generator._move_incidents_to_end_of_list(infolist_one)
        expected = 2
        result = zip_generator._get_incidents_idx(infolist_one)
        self.assertEqual(result, expected)

        zip_generator._move_incidents_to_end_of_list(infolist_two)
        expected = 1
        result = zip_generator._get_incidents_idx(infolist_two)
        self.assertEqual(result, expected)

    def test_extract_zip(self):
        """Are zips yielded as intended"""
        zip_generator = ZipGenerator('KS', 2017)
        zip_generator.download_zip()
        infolist = zipfile.ZipFile(io.BytesIO(zip_generator._response.content)).infolist()

        last = len(infolist) - 1
        result = None
        expected = 'KS/NIBRS_incident.csv'

        for idx, file in enumerate(zip_generator.extract_zip()):
            if idx == last:
                result = file[0]
        
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
