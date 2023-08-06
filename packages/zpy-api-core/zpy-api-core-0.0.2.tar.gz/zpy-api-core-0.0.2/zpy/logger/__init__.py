from typing import Union, Any
import logging

from enum import Enum


class ZLFormat(Enum):
    M = "%(message)s"
    NM = "%(name)s %(message)s"
    LNM = "%(name)s %(levelname)s %(message)s"
    TM = "%(asctime)s %(message)s"
    LM = "%(levelname)s - %(message)s"
    TLM = "%(asctime)s - %(levelname)s - %(message)s"
    TNLM = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_global_logger(format: str = ZLFormat.LM.value, level: int = logging.INFO):
    logging.basicConfig(format=format, level=level)


class zL(object):
    """Logger Wrapper

    Args:
        object ([type]): [description]
    """

    def __init__(self, name: str, level: int, format: Union[str, ZLFormat]) -> None:
        self._logger = logging.getLogger(name)
        for h in self._logger.handlers:
            self._logger.removeHandler(h)
        self._logger.setLevel(level)
        self._level = level
        self.formatter = logging.Formatter(
            format if isinstance(format, str) else format.value
        )
        self._handler = logging.StreamHandler()
        self._handler.setLevel(self._level)
        self._handler.setFormatter(self.formatter)
        self._logger.addHandler(self._handler)
        self._logger.propagate = False

    @classmethod
    def create(cls, name: str):
        return cls(name, logging.INFO, ZLFormat.TNLM)

    @classmethod
    def create_for_cloud(cls, name: str):
        return cls(name, logging.INFO, ZLFormat.LM)

    def raw(self, value: Any, *args):
        self._logger.log(self._level, value, *args)

    @staticmethod
    def w(msg: object, *args):
        logging.warning(msg=msg, *args)

    @staticmethod
    def i(msg: object, *args):
        """Information Level Log

        Args:
            msg (object): value
        """
        logging.info(msg=msg, *args)

    @staticmethod
    def e(msg: object, exc_info=None, *args):
        """Error Level Log

        Args:
            @param msg:
            @param exc_info:
        """
        logging.error(msg=msg, exc_info=exc_info, *args)

    @staticmethod
    def ex(msg: object, *args):
        """Exception Level Log

        Args:
            msg (object): value
        """
        logging.exception(msg=msg, *args)

    @staticmethod
    def d(msg: object, *args):
        """Debug Level Log

        Args:
            msg (object): value
        """
        logging.debug(msg=msg, *args)
