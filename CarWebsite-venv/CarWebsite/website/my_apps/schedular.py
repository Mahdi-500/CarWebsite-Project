from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import requests
from website.models import GeneralInformation
from io import BytesIO
from rest_framework.parsers import JSONParser
logger = logging.getLogger(__name__)

def GeneralInformation_Model_Updater():
    attrs = ["bodies.type", "engines.cylinders", "engines.drive_type", "engines.engine_type", 
                "engines.fuel_type", "engines.transmission", "engines.valves"]
    data_dict = {}
    for i in attrs:
        url = "https://carapi.app/api/vehicle-attributes?attribute="
        url += i
        recieved = requests.get(url)
        r = BytesIO(recieved.content)
        parser  = JSONParser()
        data = parser.parse(stream=r)
        data_dict[i] = data

    GeneralInformation.objects.update_or_create(info={"body_types":data_dict["bodies.type"],
                                                    "cylinders":data_dict["engines.cylinders"],
                                                    "drive_types":data_dict["engines.drive_type"],
                                                    "engine_types":data_dict["engines.engine_type"],
                                                    "fuel_types":data_dict["engines.fuel_type"],
                                                    "transmission":data_dict["engines.transmission"],
                                                    "valves":data_dict["engines.valves"]})
    logger.info("update was successful")



def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        GeneralInformation_Model_Updater,
        trigger=CronTrigger(minute="*/5"),
        id="updates the GeneralInformation model every 5 minutes",
        max_instances=1,
        replace_existing=True
    )

    logger.info("added the job 'updates the GeneralInformation model every 5 minutes")

    scheduler.start()
    logger.info("job is started")