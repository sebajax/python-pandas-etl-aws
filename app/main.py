# module import
import logging.config
import sys

from infrastructure.bucket_infrastructure import BucketInfrastructure
from infrastructure.db import connect
from infrastructure.repository_infrastructure import RepositoryInfrastructure
# service import
from services.processor import BatchProcessService

# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)

logger.info("---------------------------------------")
logger.info("batch process started")

file = sys.argv[1]

# wire dependencies
bucket_infrastructure = BucketInfrastructure(file)
repository_infrastructure = RepositoryInfrastructure(connect())

# create batch instance
batch_process_service = BatchProcessService(file, bucket_infrastructure, repository_infrastructure)

# call process
response = batch_process_service.process()

logger.info(response)

logger.info("batch process ended")
logger.info("---------------------------------------")
