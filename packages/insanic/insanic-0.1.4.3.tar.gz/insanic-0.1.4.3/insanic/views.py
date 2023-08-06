from sanic.response import json, HTTPResponse
from sanic.views import HTTPMethodView

from insanic.http import HTTP_STATUS

__all__ = (
    'View',
)


class View(HTTPMethodView):
    def response(self, data: dict, http_status:int = HTTP_STATUS.OK) -> HTTPResponse:  # pylint: disable=no-self-use
        response_data = { 'status': 'ok', 'data': data }
        return json(response_data, status=http_status)
