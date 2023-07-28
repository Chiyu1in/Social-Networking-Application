import uvicorn
import time

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from pytz import timezone
from jose import jwt

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# from az_redis.utils import get_redis
from routers import authentication, user, board, post
from watch_dog import watch

from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
from opencensus.trace.span import SpanKind
from opencensus.trace.attributes_helper import COMMON_ATTRIBUTES

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


KVUri = f"https://ptt-app-stage.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)


JWT_SECRET_KEY = client.get_secret('JWT-SECRET-KEY').value
InstrumentationKey = client.get_secret('APP-INSIGHT-KEY').value

SECRET_KEY = JWT_SECRET_KEY
ALGORITHM = "HS256"

tracer = Tracer(
    exporter=AzureExporter(
        connection_string=f'InstrumentationKey={InstrumentationKey}'),
    sampler=ProbabilitySampler(1.0),
)
HTTP_URL = COMMON_ATTRIBUTES["HTTP_URL"]
HTTP_ROUTE = COMMON_ATTRIBUTES["HTTP_ROUTE"]
HTTP_METHOD = COMMON_ATTRIBUTES["HTTP_METHOD"]
HTTP_STATUS_CODE = COMMON_ATTRIBUTES["HTTP_STATUS_CODE"]

app = FastAPI()

origins = [
    'https://ptt-app.azurewebsites.net',
    'https://ptt-app-stage.azurewebsites.net',
    'https://ptt-app-prod.azurewebsites.net',
    'http://localhost',
    'http://localhost:8080',
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(board.router)
app.include_router(post.router)


@app.on_event("startup")
async def startup_event():
    scheduler = BackgroundScheduler()
    scheduler.add_job(watch, 'interval', seconds=10)
    scheduler.start()

@app.middleware("http")
async def middlewareOpencensus(request: Request, call_next):
    start_time = time.time()
    
    try:
        token = request.headers.get('authorization').split()[-1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except:
        user_id = None

    with tracer.span(name="test") as span:
        span.span_kind = SpanKind.SERVER

        response = await call_next(request)
            
        tracer.add_attribute_to_current_span(
            attribute_key=HTTP_STATUS_CODE, attribute_value=response.status_code
        )
        tracer.add_attribute_to_current_span(
            attribute_key=HTTP_METHOD, attribute_value=str(request.method)
        )
        tracer.add_attribute_to_current_span(
            attribute_key=HTTP_URL, attribute_value=str(request.url)
        )
        tracer.add_attribute_to_current_span(
            attribute_key=HTTP_ROUTE, attribute_value=str(request.url.path)
        )
        tracer.add_attribute_to_current_span(
            attribute_key='user_id', attribute_value=user_id
        )

        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(round(process_time, 4))

    return response

@app.get('/')
def hello_word():
    return 'hello_word'

def get_time():

    time_format = '%Y-%m-%d %H:%M:%S'
    cur_time = datetime.now(timezone('Asia/Taipei'))

    return cur_time.strftime(time_format)


if __name__ == '__main__':

    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)