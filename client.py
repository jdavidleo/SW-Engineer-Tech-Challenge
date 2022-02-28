import asyncio
import time
import requests
import httpx
import json
from bson import json_util
from pydicom import Dataset
from scp import ModalityStoreSCP

API_ENDPOINT = "http://localhost:5000"

class SeriesCollector:
    """A Series Collector is used to build up a list of instances (a DICOM series) as they are received by the modality.
    It stores the (during collection incomplete) series, the Series (Instance) UID, the time the series was last updated
    with a new instance and the information whether the dispatch of the series was started.
    """
    def __init__(self, first_dataset: Dataset) -> None:
        """Initialization of the Series Collector with the first dataset (instance).

        Args:
            first_dataset (Dataset): The first dataset or the regarding series received from the modality.
        """
        self.series_instance_uid = first_dataset.SeriesInstanceUID
        self.series: list[Dataset] = [first_dataset]
        self.last_update_time = time.time()
        self.dispatch_started = False

    def add_instance(self, dataset: Dataset) -> bool:
        """Add an dataset to the series collected by this Series Collector if it has the correct Series UID.

        Args:
            dataset (Dataset): The dataset to add.

        Returns:
            bool: `True`, if the Series UID of the dataset to add matched and the dataset was therefore added, `False` otherwise.
        """
        if self.series_instance_uid == dataset.SeriesInstanceUID:
            self.series.append(dataset)
            self.last_update_time = time.time()
            return True

        return False


class SeriesDispatcher:
    """This code provides a template for receiving data from a modality using DICOM.
    Be sure to understand how it works, then try to collect incoming series (hint: there is no attribute indicating how
    many instances are in a series, so you have to wait for some time to find out if a new instance is transmitted).
    For simplyfication, you can assume that only one series is transmitted at a time.
    You can use the given template, but you don't have to!
    """

    def __init__(self) -> None:
        """Initialize the Series Dispatcher.
        """

        self.loop: asyncio.AbstractEventLoop
        self.modality_scp = ModalityStoreSCP()
        self.series_collector = None

    async def main(self) -> None:
        """An infinitely running method used as hook for the asyncio event loop.
        Keeps the event loop alive whether or not datasets are received from the modality and prints a message
        regulary when no datasets are received.
        """
        while True:
            # TODO: Regulary check if new datasets are received and act if they are.
            # Information about Python asyncio: https://docs.python.org/3/library/asyncio.html
            # When datasets are received you should collect and process them
            # (e.g. using `asyncio.create_task(self.run_series_collector()`)
            
            #if dataset stack has data.
            if(len(self.modality_scp.datasets)>0):
                print("Modality arrived!")
                asyncio.create_task(self.run_series_collectors()) #collect data
            
            asyncio.create_task(self.dispatch_series_collector()) #dispatch any data that reside in series collector and hasn't been dispatched
                
            print("Waiting for Modality")
            await asyncio.sleep(0.2)

    async def run_series_collectors(self) -> None:
        """Runs the collection of datasets, which results in the Series Collector being filled.
        """
        # TODO: Get the data from the SCP and start dispatching
        dataset = self.modality_scp.datasets.pop()#extract 
        if self.series_collector is None:
            self.series_collector = SeriesCollector(dataset)
        else:
            is_instance = self.series_collector.add_instance(dataset)
            if not is_instance:
                self.modality_scp.datasets.append(dataset)
        pass

    async def dispatch_series_collector(self) -> None:
        """Tries to dispatch a Series Collector, i.e. to finish it's dataset collection and scheduling of further
        methods to extract the desired information.
        """
        # Check if the series collector hasn't had an update for a long enough timespan and send the series to the
        # server if it is complete
        # NOTE: This is the last given function, you should create more for extracting the information and
        # sending the data to the server
        maximum_wait_time = 1
        if self.series_collector is None:
            return
        if (time.time() - self.series_collector.last_update_time)> maximum_wait_time:
            if(not self.series_collector.dispatch_started):
                info = self.extract_info()
                self.series_collector.dispatch_started=True
                await self.send_2_server(info)
                self.series_collector = None
                self.modality_scp.unread_event=False
        pass

    def extract_info(self):
        info = {}
        info['SeriesInstanceUID']=self.series_collector.series[0].SeriesInstanceUID
        info['PatientName']=str(self.series_collector.series[0].PatientName)
        info['PatientID']=self.series_collector.series[0].PatientID
        info['StudyInstanceUID']=self.series_collector.series[0].StudyInstanceUID
        info['InstancesInSeries']=len(self.series_collector.series)

        return info

    async def send_2_server(self, info):
        async with httpx.AsyncClient() as client:
            r = await client.post(API_ENDPOINT+'/dicom', json = info)
        #body = json.dumps(info, default=json_util.default)
        #r = requests.post(API_ENDPOINT+'/dicom', json=info)
        print("request sent: "+str(r.status_code))
        pass


if __name__ == "__main__":
    """Create a Series Dispatcher object and run it's infinite `main()` method in a event loop.
    """
    engine = SeriesDispatcher()
    engine.loop = asyncio.get_event_loop()
    engine.loop.run_until_complete(engine.main())
