from fastapi import FastAPI
from titiler.core.factory import TilerFactory
from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers


app = FastAPI(title="Cloud Tiler Service")

# attach TiTiler router under /cog prefix
cog = TilerFactory()
app.include_router(cog.router, prefix="/cog", tags=["Cloud Optimized GeoTIFF"])

# secure standard geospatial error handlers
add_exception_handlers(app, DEFAULT_STATUS_CODES)

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "TiTiler Cloud Worker"}