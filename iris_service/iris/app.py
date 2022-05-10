from operator import imod
from fastapi import FastAPI, Response, Request, status
from starlette.responses import JSONResponse
from iris.router import iris_classifier_router
import prometheus_client
from prometheus_client import generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST, Counter
from starlette_prometheus import metrics, PrometheusMiddleware


# start_http_server(5000)
app = FastAPI()
app.include_router(iris_classifier_router.router, prefix='/iris')
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)


graphs = {}
graphs["count"] = Counter("python_total_request", "Number of requests")   

@app.get('/healthcheck', status_code=200)
async def healthcheck():
    graphs["count"].inc()
    return 'Iris classifier is all ready to go!'

# @app.get('/metrics', status_code=200)
# async def metrics():
#     return Response(prometheus_client.generate_latest(), media_type=CONTENT_TYPE_LATEST)

# curl 'http://localhost:8080/iris/classify_iris' -X POST -H 'Content-Type: application/json' -d '{"sepal_length": 5, "sepal_width": 2, "petal_length": 3, "petal_width": 4}'