from tracepointdebug.tracepoint.trace_point_manager import TracePointManager
from tracepointdebug.broker.handler.response.response_handler import ResponseHandler
from tracepointdebug.tracepoint.response import FilterTracePointsResponse

from tracepointdebug.application.application import Application


def _applyTracePoint(trace_point):
    try:
        condition = trace_point.get("condition", None)
        client = trace_point.get("client", None)
        file_name = trace_point.get("fileName", None)
        trace_point_manager = TracePointManager.instance()
        trace_point_manager.put_trace_point(trace_point.get("id", None), file_name, 
                                            trace_point.get("fileHash", None), trace_point.get("lineNo",None),
                                            client, trace_point.get("expireDuration", None), trace_point.get("expireCount", None),
                                            trace_point.get("disabled", None), condition = condition)
        
        trace_point_manager.publish_application_status()
        if client is not None:
            trace_point_manager.publish_application_status(client)

    except Exception as e:
        print(e)

class FilterTracePointsResponseHandler(ResponseHandler):
    RESPONSE_NAME = "FilterTracePointsResponse"


    @staticmethod
    def get_response_name():
        return FilterTracePointsResponseHandler.RESPONSE_NAME

    
    @staticmethod
    def get_response_cls():
        return FilterTracePointsResponse


    @staticmethod
    def handle_response(response):
        trace_points = response.trace_points
        for trace_point in trace_points:
            _applyTracePoint(trace_point)
    