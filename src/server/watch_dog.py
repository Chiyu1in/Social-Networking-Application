from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
from opencensus.trace.span import SpanKind
from opencensus.trace.attributes_helper import COMMON_ATTRIBUTES

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

from database.utils import get_db
from routers import user, board
from schema import UserIn, BoardInfo, UserBoardInfo

KVUri = f"https://ptt-app-stage.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

InstrumentationKey = client.get_secret('APP-INSIGHT-KEY').value
tracer = Tracer(
    exporter=AzureExporter(
        connection_string=f'InstrumentationKey={InstrumentationKey}'),
    sampler=ProbabilitySampler(1.0),
)

HTTP_URL = COMMON_ATTRIBUTES["HTTP_URL"] 
HTTP_METHOD = COMMON_ATTRIBUTES["HTTP_METHOD"]
HTTP_STATUS_CODE = COMMON_ATTRIBUTES["HTTP_STATUS_CODE"]

def watch():

    trace_watch(
        user.has_user(UserIn(username='aics_admin1'), next(get_db())),
        '/has_user/'
    )
    trace_watch(
        board.is_latest_unread(UserBoardInfo(user='aics_admin1', board='NBA'), next(get_db())),
        '/is_latest_unread/'
    )
    trace_watch(
        board.count_likes(BoardInfo(board='NBA'), next(get_db())),
        '/count_likes/'
    )
    trace_watch(
        board.get_latest_post(BoardInfo(board='NBA'), next(get_db())),
        '/read_latest_post/'
    )
import asyncio
def trace_watch(task, path):
    with tracer.span(name="WATCH") as span:
        span.span_kind = SpanKind.SERVER

        tracer.add_attribute_to_current_span(
                attribute_key=HTTP_METHOD, attribute_value='WATCH'
            )
        tracer.add_attribute_to_current_span(
            attribute_key=HTTP_URL, attribute_value=path
        )
        try:
            asyncio.run(task)
            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_STATUS_CODE, attribute_value=200 
            )
        except:
            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_STATUS_CODE, attribute_value=404
            )