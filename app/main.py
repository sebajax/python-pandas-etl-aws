# module import
import sys
import logging

from bucket_infrastructure import BucketInfrastructure
# service import
from processor import BatchProcessService

# get root logger
logger = logging.getLogger(__name__)

logger.info("batch process started")

file = sys.argv[1]

# wire dependencies
bucket_infrastructure = BucketInfrastructure(file)

# create batch instance
batch_process_service = BatchProcessService(file, bucket_infrastructure)

# call process
response = batch_process_service.process()

print(response)

logger.info("batch process ended")
