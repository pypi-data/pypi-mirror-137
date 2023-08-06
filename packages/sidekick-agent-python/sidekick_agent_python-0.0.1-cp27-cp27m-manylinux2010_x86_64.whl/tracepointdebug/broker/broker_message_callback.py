import json

from tracepointdebug.tracepoint.encoder import to_json
from tracepointdebug.tracepoint.handler import ( DisableTracePointRequestHandler, 
    EnableTracePointRequestHandler, PutTracePointRequestHandler, RemoveTracePointRequestHandler, 
    UpdateTracePointRequestHandler, FilterTracePointsResponseHandler )


MESSAGE_REQUEST_TYPE = "Request"
MESSAGE_RESPONSE_TYPE = "Response"

REQUEST_HANDLER_MAP = {
    "DisableTracePointRequest": DisableTracePointRequestHandler,
    "EnableTracePointRequest": EnableTracePointRequestHandler,
    "PutTracePointRequest": PutTracePointRequestHandler,
    "RemoveTracePointRequest": RemoveTracePointRequestHandler,
    "UpdateTracePointRequest": UpdateTracePointRequestHandler
}

RESPONSE_HANDLER_MAP = {
    "FilterTracePointsResponse": FilterTracePointsResponseHandler
}


class BrokerMessageCallback(object):

    def on_message(self, broker_client, message):
        try:
            message = json.loads(message)

            message_type = message.get("type", None)

            if message_type == MESSAGE_REQUEST_TYPE:
                handler = REQUEST_HANDLER_MAP.get(message.get("name"))
                if handler is not None:
                    request = handler.get_request_cls()(message)
                    response = handler.handle_request(request)
                    serialized = to_json(response)
                    broker_client.send(serialized)
                else:
                    print("No request handler could be found for message with name {}: {}".format(message.get("name"),
                                                                                              message))
            elif message_type == MESSAGE_RESPONSE_TYPE:
                handler = RESPONSE_HANDLER_MAP.get(message.get("name"))
                if handler is not None:
                    response = handler.get_response_cls()(**message)
                    handler.handle_response(response)
                else:
                    print("No response handler could be found for message with name {}: {}".format(message.get("name"),
                                                                                              message))

        except Exception as e:
            print(e)
