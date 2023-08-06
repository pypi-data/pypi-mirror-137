from tracepointdebug.broker.request.base_request import BaseRequest

from uuid import uuid4
from typing import Dict

class FilterTracePointsRequest(BaseRequest):
    

    def __init__(self, name, version, stage, customTags):
        super(FilterTracePointsRequest, self).__init__(str(uuid4()))
        self._application_filter = ApplicationFilter()
        self._application_filter.name = name
        self._application_filter.version = version
        self._application_filter.stage = stage
        self._application_filter.custom_tags = customTags

    def get_id(self):
        return self._id


    def get_name(self):
        return self.__class__.__name__

    
    @property
    def application_filter(self):
        return self._application_filter

    
    @application_filter.setter
    def application_filter(self, application_filter):
        self._application_filter = application_filter


    def to_json(self):
        return { 
                "type": self.get_type(),
                "name": self.get_name(),
                "id": self.id,
                "applicationFilter": self.application_filter,
                "applicationFilterName": self.application_filter.name,
                "applicationFilterStage": self.application_filter.stage,
                "applicationFilterVersion": self.application_filter.version,
                "applicationFilterCustomTags": self.application_filter.custom_tags,
            }


class ApplicationFilter:

    @property
    def name(self):
        return self._name


    @name.setter
    def name(self, name):
        self._name = name    

    
    @property
    def stage(self):
        return self._stage

    
    @stage.setter
    def stage(self, stage):
        self._stage = stage


    @property
    def version(self):
        return self._version


    @version.setter
    def version(self, version):
        self._version = version


    @property
    def custom_tags(self):
        return self._custom_tags

    
    @custom_tags.setter
    def custom_tags(self, custom_tags):
        self._custom_tags = custom_tags


    def to_json(self):
        return {
                "name": self.name,
                "stage": self.stage,
                "version": self.version,
                "customTags": self.custom_tags
            }