from shiny import App, ui
from fastapi import FastAPI
from titiler.core.factory import TilerFactory
from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers
import re

# 1. Initialize the FastAPI instance and the TiTiler Factory
tiler_fastapi_app = FastAPI()
cog = TilerFactory()
tiler_fastapi_app.include_router(cog.router, prefix="/cog", tags=["COG"])
add_exception_handlers(tiler_fastapi_app, DEFAULT_STATUS_CODES)

app_ui = ui.page_fluid(
    ui.h3("Dynamic Map Tiler Gateway"),
    ui.p("Geospatial routing container active.")
)

def server(input, output, session):
    pass

shiny_app = App(app_ui, server)

# 3. Custom ASGI routing + clean URL intercept middleware
async def custom_asgi_app(scope, receive, send):
    if scope["type"] == "http":
        path = scope["path"]
        
        # Look for legacy or clean short paths: /cog/tiles/{z}/{x}/{y}.png
        # and rewrite the scope path variables to match TiTiler's expected structure
        match = re.match(r"^/cog/tiles/(\d+)/(\d+)/(\d+)(\.\w+)?$", path)
        if match:
            z, x, y, ext = match.groups()
            ext = ext if ext else ".png"
            # Translate path seamlessly behind the scenes to WebMercatorQuad
            scope["path"] = f"/cog/tiles/WebMercatorQuad/{z}/{x}/{y}{ext}"

        # Route to FastAPI if it starts with our target prefix
        if scope["path"].startswith("/cog"):
            await tiler_fastapi_app(scope, receive, send)
            return

    # Fallback to Shiny app UI
    await shiny_app(scope, receive, send)

app = custom_asgi_app