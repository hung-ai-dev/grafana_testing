import sys
import logging
from fastapi import APIRouter
from starlette.responses import JSONResponse
from prometheus_client import start_http_server, Summary, Counter
import logging_loki

from iris.iris_classifier import IrisClassifier
from iris.models import Iris

logging_loki.emitter.LokiEmitter.level_tag = "level"
# assign to a variable named handler 
# handler = logging_loki.LokiHandler(
#    url="http://localhost:3100/loki/api/v1/push",
#    version="1",
# )

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(stream = sys.stdout, 
                    filemode = "w",
                    format = Log_Format, 
                    level = logging.ERROR)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# logger.addHandler(handler)
router = APIRouter()
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
c = Counter('predict_total_request', 'Number of requests')

# Decorate function with metric.
@REQUEST_TIME.time()
@router.post('/classify_iris')
def extract_name(iris_features: Iris):
    logger.info(f"Logger: Classify object", 
                extra={"tags": {"service": "iris:info"}},)
    iris_classifier = IrisClassifier()
    c.inc()
    print("Print: Classify object")
    return JSONResponse(iris_classifier.classify_iris(iris_features))