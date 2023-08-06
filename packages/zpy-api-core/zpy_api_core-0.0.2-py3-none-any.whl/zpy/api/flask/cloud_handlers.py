import logging
from typing import Callable
from zpy.containers import shared_container
from zpy.api.http.response import _useAwsRequestId
from zpy.utils.values import if_null_get
from timeit import default_timer as timer
from datetime import timedelta
from functools import wraps


def store_request_id(context):
    """Extract aws request id from context

    Args:
        context ([type]): Lambda context
    """
    try:
        shared_container["aws_request_id"] = context.aws_request_id
    except Exception as e:
        logging.exception("An error occurred while extracting aws request id")


def event_processors(useId: bool, logs: bool, *args, **kwargs):
    """Lambda event processors

    Args:
        useId (bool): Register request id
        logs (bool): Logging event data
    """
    try:
        if len(args) >= 2:
            event = args[0]
            if logs:
                print(f"Request:\n {event}")
            if _useAwsRequestId or useId:
                store_request_id(args[1])
        else:
            if "event" in kwargs:
                if logs:
                    print(f"Request:\n {kwargs['event']}")
            if "context" in kwargs:
                if _useAwsRequestId:
                    store_request_id(args[1])
    except:
        pass


def aws_lambda(logs: bool = True, save_id: bool = False, measure_time: bool = True):
    """Lambda Handler

    Args:
        logs (bool, optional): Logging request and response. Defaults to False.
        save_id (bool, optional): Register aws lambda request id. Defaults to True.
        measure_time (bool, optional): Measure elapsed execution time. Defaults to True.
    """

    def callable(invoker: Callable):
        @wraps(invoker)
        def wrapper(*args, **kwargs):
            event_processors(save_id, logs, *args, **kwargs)
            if if_null_get(measure_time, False):
                start = timer()
            result = invoker(*args, **kwargs)
            if logs:
                print(f"Response: {result}")
            if if_null_get(measure_time, False):
                end = timer()
                print(f"Elapsed execution time: {timedelta(seconds=end - start)}")
            return result

        return wrapper

    return callable
