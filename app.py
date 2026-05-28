from shiny import App, ui
from fastapi import FastAPI, Request
from titiler.core.factory import TilerFactory
from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers
from starlette.middleware.base import BaseHTTPMiddleware
import re

# initialize FastAPI app
app = FastAPI()

class CleanUrlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        # Look for legacy or clean short paths: /cog/tiles/{z}/{x}/{y}.png
        match = re.match(r"^/cog/tiles/(\d+)/(\d+)/(\d+)(\.\w+)?$", path)
        if match:
            z, x, y, ext = match.groups()
            ext = ext if ext else ".png"
            # Modify the scope path before passing it down the line
            request.scope["path"] = f"/cog/tiles/WebMercatorQuad/{z}/{x}/{y}{ext}"
        
        response = await call_next(request)
        return response

app.add_middleware(CleanUrlMiddleware)

# include TiTiler Router under /cog
cog = TilerFactory()
app.include_router(cog.router, prefix="/cog", tags=["COG"])
add_exception_handlers(app, DEFAULT_STATUS_CODES)

# simple shiny App UI and Server
app_ui = ui.page_fluid(
    ui.h3("Dynamic Map Tiler Gateway"),
    ui.p("Geospatial routing container active.")
)

def server(input, output, session):
    pass

shiny_app = App(app_ui, server)

# mount shiny App to the root of FastAPI
app.mount("/", shiny_app)