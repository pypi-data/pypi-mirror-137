# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

import contrast

from aiohttp.web import StreamResponse

from contrast.agent.request_context import RequestContext
from contrast.agent.asgi import aiohttp_request_to_environ
from contrast.agent import scope as scope_manager
from contrast.extern import structlog as logging
from contrast.utils.decorators import log_time_cm
from contrast.utils.exceptions.contrast_service_exception import (
    ContrastServiceException,
)
from contrast.agent.middlewares.base_middleware import BaseMiddleware
from contrast.utils.decorators import fail_safely

logger = logging.getLogger("contrast")


class AioHttpMiddleware(BaseMiddleware):
    __middleware_version__ = 1  # Aiohttp new-style middleware

    # Since there is no way to get the `app` instance, on startup of AioHttp,
    # until the first request, hence we will not have `app` finder logic.
    def __init__(self, app_name: str = None) -> None:
        self.app = None
        self.app_name = app_name
        super().__init__()

    async def __call__(self, request, handler) -> StreamResponse:
        self.app = request.app

        if self.is_agent_enabled():
            with scope_manager.contrast_scope():
                # aiohttp_request_to_environ fails because we don't ever get a request body and
                # we don't get the scope (request.scope doesn't exist unlike in fastapi)
                environ = await aiohttp_request_to_environ(request)

            context = RequestContext(environ)

            with contrast.CS__CONTEXT_TRACKER.lifespan(context):
                return await self.call_with_agent(context, request, handler)

        return await self.call_without_agent_async(request, handler)

    async def call_with_agent(self, context, request, handler) -> StreamResponse:
        self.log_start_request_analysis(request.path)

        # TODO: PYT-1909 uncomment when we start to implement assess sources
        # track_scope_sources(context, scope)
        try:
            self.prefilter(context)

            with log_time_cm("app code and get response"):
                response = await handler(request)

            with scope_manager.contrast_scope():
                # TODO: PYT-1914 We had a custom FastAPI class for this. We should investigate if theres
                #  anything else we need to do here
                # wrapped_response = context.extract_response_to_context(response)
                pass

            # TODO: PYT-1914
            # await self.extract_response_to_context_async(wrapped_response, context)
            # self.postfilter(context)

            self.check_for_blocked(context)
            return response

        except ContrastServiceException as e:
            logger.warning(e)
            return await self.call_without_agent_async(request, handler)
        except Exception as e:
            response = self.handle_exception(e)
            return response
        finally:
            self.handle_ensure(context, context.request)
            self.log_end_request_analysis(context.request.path)
            # TODO: PYT-1909 uncomment when assess sources are added
            # if self.settings.is_assess_enabled():
            #     contrast.STRING_TRACKER.ageoff()

    async def call_without_agent_async(self, request, handler) -> StreamResponse:
        super().call_without_agent()
        return await handler(request)

    @fail_safely("Unable to get route coverage", return_value={})
    def get_route_coverage(self):
        pass
