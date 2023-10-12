# module import
import sys
import logging
# service import
from processor import BatchProcessService

# get root logger
logger = logging.getLogger(__name__)

logger.info("batch process started")

file = sys.argv[1]

batch_process_service = BatchProcessService(file)

response = batch_process_service.process()

print(response)

logger.info("batch process ended")
