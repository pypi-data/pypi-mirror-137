from marshmallow_objects import models
from marshmallow.exceptions import ValidationError
from typing import Dict, List, Tuple, Union
from zpy.api.http.errors import BadRequest, ZHttpError
from zpy.utils.objects import ZObjectModel


def parse_request(
    request: dict, model: ZObjectModel, raisable: bool = True
) -> Tuple[ZObjectModel, ZHttpError]:
    """
    Parse and validate request acordning model specification

    Parameters
    ----------
    request : dict | required
        Request object to validate

    model : ZObjectModel | required
        The model specification

    Raises
    ------
    NotValueProvided
        If no values is set for the response or passed in as a parameter.

    Returns
    -------
    (model,errors) : Tuple[models.Model, Dict]
        Tuple with model and erros either the validation process

    """

    model_result: Union[List, ZObjectModel] = None
    errors: Union[List, None] = None
    try:
        if request == None or len(request.items()) == 0:
            error = BadRequest(
                "The request was not provided, validation request error",
                f"Missing fields {model().__missing_fields__} not provided",
            )
            if raisable:
                raise error
            return None, error
        model_result = model(**request)
    except ValidationError as e:
        model_result = e.valid_data
        if isinstance(e.messages, Dict):
            errors = [e.messages]
        else:
            errors = e.messages
        errors = BadRequest(None, f"Missing fields {errors} not provided")
        if raisable:
            raise errors
    return model_result, errors
