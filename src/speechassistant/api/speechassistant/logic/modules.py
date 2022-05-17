from __future__ import annotations

import json
import os
import pkgutil
from pathlib import Path

from flask import Response


def create_module(data: dict) -> Response:
    return Response(status=404)


def read_module(name: str) -> Response:
    return Response(status=404)


def read_modules() -> Response:
    return Response(status=404)


def read_module_names() -> Response:
    module_names = []
    module_path = Path(os.path.dirname(__file__)).parents[2].joinpath("modules")
    for finder, name, ispkg in pkgutil.walk_packages([str(module_path)]):
        module_names.append(name)
    return Response(
        json.dumps({"names": module_names}), mimetype="application/json", status=200
    )


def update_module(data: dict) -> Response:
    return Response(status=404)


def delete_module(data: dict) -> Response:
    return Response(status=404)
