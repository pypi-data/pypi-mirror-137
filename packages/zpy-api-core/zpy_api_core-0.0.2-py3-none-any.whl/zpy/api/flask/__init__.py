from typing import Any, List, Optional, Dict
from flask_cors import CORS

from flask import Flask

from zpy.api.flask.zhooks import ZHook
from zpy.api.flask.zmiddlewares import ZMiddleware


def create_flask_app(
        config: dict,
        main_path: str,
        path_cors_allow=None,
) -> Flask:
    """
    API Builder
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    path_allow = path_cors_allow
    if path_cors_allow is None:
        path_allow = r"{}{}".format(main_path, "/*")
    CORS(app, resources={path_allow: {"origins": "*"}})
    return app


def create_app(app: Optional[Flask] = None, mw: Optional[List[ZMiddleware]] = None, mw_args=None,
               hk: Optional[List[ZHook]] = None,
               hk_args=None,
               shared_data: Dict[Any, Any] = None, path_cors_allow=None, ) -> Optional[Flask]:
    if hk_args is None:
        hk_args = []
    if mw_args is None:
        mw_args = []
    if shared_data is None:
        shared_data = {}
    if hk is None:
        hk = []
    if mw is None:
        mw = []
    if app is None:
        app = create_flask_app(shared_data, "/", path_cors_allow)

    for i, m in enumerate(mw):
        args = mw_args[i] if i < len(mw_args) else {}
        args.update(shared_data)
        app.wsgi_app = m(app.wsgi_app, **args)
    for i, h in enumerate(hk):
        args = hk_args[i] if i < len(hk_args) else {}
        args.update(shared_data)
        h().execute(app, **args)

    return app
