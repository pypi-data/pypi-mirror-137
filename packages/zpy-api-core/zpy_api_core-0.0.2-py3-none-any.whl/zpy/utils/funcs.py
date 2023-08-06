from typing import Any, Callable, List, Optional
import logging


def safely_exec(callable_fn: Callable, args=None) -> Optional[Any]:
    """
    Execute provided function in try:except block
    @param callable_fn:
    @param args:
    @return: value returned of execution or none
    """
    if args is None:
        args = []
    try:
        return callable_fn(*args)
    except Exception as e:
        logging.exception(e)
    return None


def exec_if_nt_null(callable_fn: Callable, args: Optional[List[Any]] = None) -> object:
    """
    Execute function if args not null
    """
    if args is None:
        args = []
    for arg in args:
        if arg is None:
            return False
    return callable_fn(*args)


def safely_exec_with(callable_fn: Callable, default_value: Any = None, args=None) -> Optional[Any]:
    """
    Execute provided function in try:except block
    @param default_value:
    @param callable_fn:
    @param args:
    @return: value returned of execution or none
    """
    if args is None:
        args = []
    try:
        return callable_fn(*args)
    except Exception as e:
        logging.exception(e)
    return default_value
