class EsStatsException(Exception):
    """
    Base class for all exceptions raised by es_stats which are not Elasticsearch
    exceptions.
    """

class ConfigurationError(EsStatsException):
    """
    Exception raised when a misconfiguration is detected
    """

class MissingArgument(EsStatsException):
    """
    Exception raised when a needed argument is not passed.
    """

class NotFound(EsStatsException):
    """
    Exception raised when expected information is not found.
    """

class FailedExecution(EsStatsException):
    """
    Exception raised when an action fails to execute for some reason.
    """
