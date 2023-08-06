"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

from . import JsonObject, JsonList
from appd.time import from_ts

class MetricValue(JsonObject):

    FIELDS = {
        'occurrences': '',
        'current': '',
        'min': '',
        'max': '',
        'start_time_ms': 'startTimeInMillis',
        'count': '',
        'sum': '',
        'value': '',
        'std_dev': 'standardDeviation'
    }

    def __init__(self, occurrences=0, current=0, min_value=0, max_value=0, start_time_ms=0, count=0, sum=0, value=0, std_dev=0):
        (self.occurrences, self.current, self.min, self.max, self.start_time_ms, self.count, self.sum, self.value, self.std_dev) = (occurrences, current, min_value, max_value, start_time_ms, count, sum, value, std_dev)

    @property
    def start_time(self):
        """
        Gets the timestamp of the metric data, converting it from an AppDynamics timestamp to standard
        Python :class:`datetime`.

        :return: Time the violation was resolved
        :rtype: :class:`datetime.datetime`
        """
        return from_ts(self.start_time_ms)


class MetricValues(JsonList):

    def __init__(self, initial_list=None):
        super(MetricValues, self).__init__(MetricValue, initial_list)

    def __getitem__(self, i):
        """
        :rtype: MetricValue
        """
        return self.data[i]
