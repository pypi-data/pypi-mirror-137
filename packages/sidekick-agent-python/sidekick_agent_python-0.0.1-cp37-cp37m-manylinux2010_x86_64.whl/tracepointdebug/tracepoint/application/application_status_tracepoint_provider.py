import abc

from tracepointdebug.tracepoint.trace_point_manager import TracePointManager
from tracepointdebug.broker.application.application_status_provider import ApplicationStatusProvider

ABC = abc.ABCMeta('ABC', (object,), {})


class ApplicationStatusTracePointProvider(ApplicationStatusProvider):

    def provide(self, application_status, client=None):
        application_status.trace_points = TracePointManager.instance().list_trace_points(client)
