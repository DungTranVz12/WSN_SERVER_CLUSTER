from _typeshed import Incomplete

from influxdb_client.service._base_service import _BaseService

class SigninService(_BaseService):
    def __init__(self, api_client: Incomplete | None = None) -> None: ...
    def post_signin(self, **kwargs): ...
    def post_signin_with_http_info(self, **kwargs): ...
    async def post_signin_async(self, **kwargs): ...
