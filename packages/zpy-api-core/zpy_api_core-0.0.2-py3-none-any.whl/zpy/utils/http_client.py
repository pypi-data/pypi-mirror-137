from enum import Enum
from typing import Any, List, Optional, Tuple, Union
from requests import post, Response
from zpy.logger import zL
from datetime import timedelta


class HLevels(Enum):
    NOTHING = -1
    URL = 1
    HEADERS = 2
    PARAMS = 3
    PAYLOAD = 4


def zhl_write(text: str, value: Any):
    def wrapper():
        if value is not None:
            zL.i(f"{text} {value}")

    return wrapper


class ZHttp:
    """HTTP Wrapper


    Raises:
        ValueError: [description]
    """

    global_options: dict = {"BASE_URL": None, "LOG_LEVEL": HLevels.NOTHING}

    @staticmethod
    def setup(base: str, log_level: HLevels) -> None:
        ZHttp.global_options["BASE_URL"] = base
        ZHttp.global_options["LOG_LEVEL"] = log_level

    @staticmethod
    def __prepare_request__(
            url, path, params, headers, data, json, log_level
    ) -> Tuple[str, HLevels]:
        final_url: str = ZHttp.global_options["BASE_URL"]
        if url is not None and path is not None:
            final_url = f"{url}{path}"
        if url is not None and path is None:
            final_url = url
        if url is None and path is not None:
            final_url = f"{final_url}{path}"

        if final_url is None:
            raise ValueError("URL not configured!")
        real_log_level = ZHttp.global_options["LOG_LEVEL"]
        try:
            data_to_log: List[Any] = [
                zhl_write(f"Start HTTP [POST] -", final_url),
                zhl_write(f"Params:", params),
                zhl_write(f"Headers:", headers),
                zhl_write(f"Body:", data if json is None else json),
            ]

            if log_level is not None:
                real_log_level = log_level

            for i in range(0, real_log_level.value):
                data_to_log[i]()
        except Exception as e:
            zL.ex("An error occurred while logging http request.")
        return final_url, real_log_level

    @staticmethod
    def __logging_response__(
            result: Response, final_url, log_response_headers, real_log_level
    ):
        parsed = result.json()
        response_logs = [
            zhl_write(f"End Http [POST] - {result.status_code}", final_url),
            zhl_write(
                f"Elapsed: {str(timedelta(seconds=result.elapsed.seconds))}",
                "",
            ),
            zhl_write(
                f"Headers:",
                dict(zip(result.headers.keys(), result.headers.values()))
                if log_response_headers is True
                else None,
            ),
            zhl_write(f"Body:", parsed),
        ]
        for i in range(0, real_log_level.value):
            response_logs[i]()

    def get(
            url: Union[str, bytes],
            params: Any = None,
            data: Any = None,
            headers: Any = None,
            cookies: Any = None,
            files: Any = None,
            auth: Any = None,
            timeout: Any = None,
            allow_redirects: bool = None,
            proxies: Any = None,
            hooks: Any = None,
            stream: Any = None,
            verify: Any = None,
            cert: Any = None,
            json: Any = None,
            verbose: bool = False,
    ):
        ...

    @staticmethod
    def post(
            url: Optional[str] = None,
            path: Optional[str] = None,
            params: Any = None,
            data: Any = None,
            headers: Any = None,
            cookies: Any = None,
            files: Any = None,
            auth: Any = None,
            timeout: Any = None,
            allow_redirects: bool = None,
            proxies: Any = None,
            hooks: Any = None,
            stream: Any = None,
            verify: Any = None,
            cert: Any = None,
            json: Any = None,
            log_level: HLevels = None,
            log_response_headers: bool = False,
            control_failure: bool = False,
    ) -> Optional[Response]:
        final_url, real_log_level = ZHttp.__prepare_request__(
            url, path, params, headers, data, json, log_level
        )
        try:
            result: Response = post(
                url=final_url,
                json=json,
                data=data,
                params=params,
                headers=headers,
                cookies=cookies,
                files=files,
                auth=auth,
                timeout=timeout,
                allow_redirects=allow_redirects,
                proxies=proxies,
                hooks=hooks,
                stream=stream,
                verify=verify,
                cert=cert,
            )
            if real_log_level != HLevels.NOTHING:
                ZHttp.__logging_response__(
                    result, final_url, log_response_headers, real_log_level
                )
            return result
        except Exception as e:
            zL.ex("The http request failed...")
            if control_failure is False:
                raise e
        return None


class ZHttpResponse(object):
    pass

    def is_ok(self) -> bool:
        # requests.codes
        return True
