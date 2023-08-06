from typing import Any, Callable, Dict, List, Optional
from zpy.utils.values import if_null_get
from datetime import datetime
from copy import copy
from marshmallow_objects import models
from marshmallow.fields import Field
from marshmallow import utils

from enum import Enum
import typing
import json

__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


def default_remove():
    return [
        "_http_status_",
        "__dump_lock__",
        "__schema__",
        "__missing_fields__",
        "__setattr_func__",
        "_ZObjectModel__remove_keys",
        "_ZObjectModel__update_items",
        "__use_native_dumps__"
    ]


class ZObjectModel(models.Model):
    """
    Zurckz Model
    """

    def __init__(
            self,
            exclude: Optional[List[str]] = None,
            include: Optional[Dict[Any, Any]] = None,
            context=None,
            partial=None,
            use_native_dumps=False,
            **kwargs
    ):
        super().__init__(context=context, partial=partial, **kwargs)
        self.__remove_keys = default_remove() + if_null_get(exclude, [])
        self.__update_items = if_null_get(include, {})
        self.__use_native_dumps__ = use_native_dumps

    def __str__(self):
        """
        Dump nested models by own properties
        """
        data = copy(self.__dict__)
        if self.__update_items is not None:
            data.update(self.__update_items)
        [data.pop(k, None) for k in self.__remove_keys]
        for k in data.keys():
            if isinstance(data[k], models.Model):
                data[k] = json.loads(str(data[k]))
            elif isinstance(data[k], list):
                data[k] = [json.loads(str(it)) for it in data[k]]
            elif isinstance(data[k], datetime):
                data[k] = str(data[k])
        return json.dumps(data)

    def zdump(self):
        """
        Dump nested models by own properties
        """
        data = copy(self.__dict__)
        if self.__update_items is not None:
            data.update(self.__update_items)
        [data.pop(k, None) for k in self.__remove_keys]
        for k in data.keys():
            if isinstance(data[k], models.Model):
                data[k] = json.loads(str(data[k]))
            elif isinstance(data[k], list):
                data[k] = [json.loads(str(it)) for it in data[k]]
            elif isinstance(data[k], datetime):
                data[k] = str(data[k])
        return data

    def ndump(
            self,
            exclude_keys: Optional[List[str]] = None,
            include: Optional[Dict[Any, Any]] = None,
            mutator: Optional[Callable[[Dict], Dict]] = None,
            map_args: Optional[List[Any]] = None,
            store_ex: bool = False,
            store_in: bool = False
    ):
        self.sdump(exclude_keys, include, mutator, map_args, store_ex, store_in, True)

    def sdump(
            self,
            exclude_keys: Optional[List[str]] = None,
            include: Optional[Dict[Any, Any]] = None,
            mutator: Optional[Callable[[Dict], Dict]] = None,
            map_args: Optional[List[Any]] = None,
            store_ex: bool = False,
            store_in: bool = False,
            use_native_dumps=False
    ):
        """
        Model dump to json safely, checking the exclude key list

        Use this function instead of zdump.

        Parameters:
        -----------

        exclude_keys: List[str], Optional,
            List of string keys of exlude in dump process
        include: Dict[Any,Any], Optional,
            Object to include in model object after exclude process before of dump process
        mutator: Callable, Optional
            Callable function to tranform object after exclude and include process
        map_args: List[Any], Optional
            Argument list to passed to map callable function
        store_ex: bool, optional
            Indicate that the exclude key added to global model exclude key array
        store_in: bool, optional
            Indicate that the include object added to global model object
        """
        data = copy(self.__dict__)

        if map_args is None:
            map_args = []

        native = use_native_dumps if use_native_dumps is True else self.__use_native_dumps__
        if native is True:
            with self.__dump_mode_on__():
                data = self.__schema__.dump(self)
        temp_exclude = copy(self.__remove_keys)
        if exclude_keys is not None:
            temp_exclude = self.__remove_keys + exclude_keys
            if store_ex:
                self.__remove_keys = self.__remove_keys + exclude_keys
        [data.pop(k, None) for k in temp_exclude]
        temp_include = copy(self.__update_items)
        if include is not None:
            temp_include.update(include)
            data.update(temp_include)
            if store_in:
                self.__update_items.update(include)
        else:
            if temp_include is not None:
                data.update(temp_include)
        if mutator is not None:
            data = mutator(data, *map_args)

        for k in data.keys():
            if isinstance(data[k], models.Model):
                data[k] = json.loads(str(data[k]))
            elif isinstance(data[k], list):
                inner_list = []
                for it in data[k]:
                    if isinstance(it, str):
                        inner_list.append(it)
                    else:
                        inner_list.append(json.loads(str(it)))
                data[k] = inner_list
            elif isinstance(data[k], datetime):
                data[k] = str(data[k])
        return data

    def build(self):
        data = copy(self.__dict__)
        if self.__update_items is not None:
            data.update(self.__update_items)
        [data.pop(k, None) for k in self.__remove_keys]
        return data


class MapMode(Enum):
    DESERIALIZATION = "D"
    SERIALIZATION = "S"
    ALL = "*"


class string(Field):
    """A string field.

    :param kwargs: The same keyword arguments that :class:`Field` receives.
    """

    #: Default error messages.
    default_error_messages = {
        "invalid": "Not a valid string.",
        "invalid_utf8": "Not a valid utf-8 string.",
    }

    def _serialize(self, value, attr, obj, **kwargs) -> typing.Optional[str]:
        if value is None:
            return None
        return self.__apply_str_mappers(
            utils.ensure_text_type(value), MapMode.SERIALIZATION
        )

    def __apply_str_mappers(self, value: str, mode: MapMode) -> str:
        try:
            if self.metadata is not None and "maps" in self.metadata:
                mutable_value: str = value
                for mapper in list(
                        filter(
                            lambda x: x["mode"] == mode.value
                                      or x["mode"] == MapMode.ALL.value,
                            self.metadata.get("maps"),
                        )
                ):
                    try:
                        mutable_value = mapper["map"](mutable_value)
                    except:
                        ...
                return mutable_value
        except Exception as _:
            ...
        return value

    def _deserialize(self, value, attr, data, **kwargs) -> typing.Any:
        if not isinstance(value, (str, bytes)):
            raise self.make_error("invalid")
        try:
            return self.__apply_str_mappers(
                utils.ensure_text_type(value), MapMode.DESERIALIZATION
            )
        except UnicodeDecodeError as error:
            raise self.make_error("invalid_utf8") from error
