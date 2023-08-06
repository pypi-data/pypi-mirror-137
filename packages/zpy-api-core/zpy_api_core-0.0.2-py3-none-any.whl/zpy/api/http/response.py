from zpy.api.http.status_codes import HttpStatus
from zpy.api.http.errors import ZHttpError
from zpy.utils.objects import ZObjectModel
from typing import Any, Callable, Tuple, Optional
from zpy.utils.values import if_null_get, is_built_type
from zpy.containers import shared_container
import logging
import json

global _useAwsRequestId
_useAwsRequestId = False
global _wrapPayloadKey
_wrapPayloadKey = None
global _useStatusFields
_useStatusFields = False
global _custom_builder
_custom_builder: Callable = None


def setup_response_builder(
        useAwsRequestId: bool = False,
        wrapPayloadKey: Optional[str] = None,
        useStatusFields: bool = False,
        custom_builder: Callable = None
):
    global _useAwsRequestId
    _useAwsRequestId = useAwsRequestId
    global _wrapPayloadKey
    _wrapPayloadKey = wrapPayloadKey
    global _useStatusFields
    _useStatusFields = useStatusFields
    global _custom_builder
    _custom_builder = custom_builder


class SuccessResponse(object):
    def __init__(self, status: HttpStatus = HttpStatus.SUCCESS) -> None:
        self._http_status_ = status


def update_error_response(response: dict) -> dict:
    return response


def update_response(
        payload: dict, status: HttpStatus = HttpStatus.SUCCESS
) -> Tuple[dict, int]:
    if _wrapPayloadKey is not None and _wrapPayloadKey != "":
        payload = {_wrapPayloadKey: payload}
    if _useStatusFields is True:
        if type(payload) is dict:
            payload.update({"code": status.value[1], "message": status.value[2]})
    if _useAwsRequestId is True:
        if type(payload) is dict and "aws_request_id" in shared_container:
            payload.update({"requestId": shared_container["aws_request_id"]})
    if _custom_builder is not None:
        payload = _custom_builder(payload, status)
    return payload, status.value[0]


def serialize_object_value(value: Any) -> dict:
    if is_built_type(value) is False:
        try:
            return value.__dict__
        except:
            return value
    else:
        try:
            return json.dumps(value)
        except:
            return value


def http_builder(invoker: Callable):
    def wrapper_handler(*args, **kwargs):
        try:

            payload: Any = invoker(*args, **kwargs)

            if issubclass(payload.__class__, (ZObjectModel)) and issubclass(
                    payload.__class__, (SuccessResponse)
            ):
                return update_response(payload.sdump(), payload._http_status_)

            if issubclass(payload.__class__, (ZObjectModel)):
                return update_response(payload.sdump())

            if issubclass(payload.__class__, (SuccessResponse)):
                return update_response(
                    serialize_object_value(payload), payload._http_status_
                )
            return update_response(serialize_object_value(payload))
        except ZHttpError as e:
            logging.exception("An error was generated when processing request.")
            http_status: HttpStatus = e.status
            return (
                update_error_response(
                    {
                        "message": if_null_get(e.message, http_status.value[2]),
                        "code": http_status.value[1],
                        "details": e.details,
                    }
                ),
                http_status.value[0],
            )
        except Exception as e:
            logging.exception(
                "An unexpected error was generated when processing request."
            )
            code: HttpStatus = HttpStatus.INTERNAL_SERVER_ERROR
            return (
                update_error_response(
                    {"message": code.value[2], "code": code.value[1], "details": None}
                ),
                code.value[0],
            )

    return wrapper_handler
