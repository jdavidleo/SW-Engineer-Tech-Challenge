import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
from isort import file

from pydicom import Dataset    
from client import SeriesCollector, SeriesDispatcher

class ClientTest(unittest.TestCase):


    def test_series_collector_not_adding_different_seriesUID(self):
        
        dataset = Dataset()
        dataset.SeriesInstanceUID='1.1.000.1.1.000.1'
        series_collector = SeriesCollector(dataset)
        dataset.SeriesInstanceUID='1.1.2.1.000.1.1.2'
        result=series_collector.add_instance(dataset)

        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()