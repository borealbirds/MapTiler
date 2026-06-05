# TiTiler Cloud Dynamic Map Tiler API (Shiny Wrapper)

This repository houses a production-ready, stateless map-tiler microservice leveraging **TiTiler** inside a **Shiny for Python ASGI wrapper** created with the assistance of LLM. 

It is specifically engineered to bypass platform constraints on environments like **Posit Connect Cloud**, which support standard Python web frameworks (like Shiny) but block raw API frameworks (like FastAPI). By routing incoming data traffic through an ASGI interceptor, this service runs as a high-performance headless tile server under a standard Shiny footprint.

## 🚀 Features

* **Posit Connect Cloud Compliant:** Disguised as a standard Shiny application to satisfy cloud platform hosting validations.
* **Custom ASGI Routing Middleware:** Intercepts incoming network requests matching the `/cog` prefix and automatically transforms clean, simple short paths (`/cog/tiles/{z}/{x}/{y}.png`) into standard OGC `WebMercatorQuad` paths behind the scenes.
* **On-the-Fly Tile Generation:** Transmutes massive multispectral and floating-point Cloud Optimized GeoTIFF (COG) files into lightweight web-standard tiles (`256x256` pixel PNGs) instantaneously via HTTP range requests.

## 📁 Repository Structure

```text
.
├── app.py              # Custom ASGI interceptor routing traffic to TiTiler or Shiny
├── test.py             # Sample map widget using the API (Local)
└── requirements.txt    # Frozen production dependencies for environment builds
```

## 🛠️ Local Development & Testing

### 1. Set Up Environment & Install Dependencies

Ensure you have Python 3.9+ installed. Create a clean virtual environment and install the required packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Tiler Gateway Locally

```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Verify the Endpoints

Open your browser and test the splitting pathways:

* **Shiny UI Fallback:** [http://127.0.0.1:8000/app](http://127.0.0.1:8000/app)
(Displays a minimal service confirmation landing page)
* **Live Clean Tile Generation:** Copy and paste the link below to verify that the intercept middleware correctly maps and colors a tile sample over network streams:

[http://127.0.0.1:8000/cog/tiles/4/2/3.png?url=http%3A%2F%2F206.12.92.143%2Fdata%2Fdashboard%2FALFL%2FAlaska%2FALFL_Alaska_2020.tif&colormap_name=ylgn](http://127.0.0.1:8000/cog/tiles/4/2/3.png?url=http%3A%2F%2F206.12.92.143%2Fdata%2Fdashboard%2FALFL%2FAlaska%2FALFL_Alaska_2020.tif&colormap_name=ylgn)

* **App Health Status Check** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

Open a second terminal window, and run the following bash script on a different port (e.g., 8500) so it doesn't conflict with the tiler:
```bash
shiny run --port 8500 test.py
```

## 🌐 Deploying to Posit Connect Cloud
Because this repo structures the application around a primary `shiny_app` object definition alongside standard requirements, you can deploy it directly via Posit Connect Cloud.

1. Push this directory to a repository on **GitHub**.
2. Log into your **Posit Connect Cloud** account dashboard.
3. Click **Publish** -> **From GitHub**
4. Choose **Shiny** as your deployment framework and select your repository. 

The platform will automatically provision the environment, download your dependencies, and expose a live, permanent public URL.

## 🔌 Frontend App Consumption Example

Once deployed, you can query your custom cloud endpoint cleanly from your main application dashboard (e.g., inside an `ipyleaflet` rendering function):

```python
import requests
from ipyleaflet import Map, TileLayer

def get_map_widget(cog_http_url):
    # Standard URL encoding prevents breaks from specialized remote paths
    encoded_cog = requests.utils.quote(cog_http_url, safe="")
    
    # Replace with your actual live Posit Connect Cloud app URL
    tiler_base_url = "[https://connect.posit.cloud/user/content/12345](https://connect.posit.cloud/user/content/12345)"
    
    # Target our clean short URL layout handled by the custom middleware
    tile_string = f"{tiler_base_url}/cog/tiles/{{z}}/{{x}}/{{y}}.png?url={encoded_cog}&colormap_name=ylgn"
    
    density_layer = TileLayer(url=tile_string, name="Dynamic Distribution Grid")
    
    m = Map(layers=[density_layer], center=[64.2, -149.5], zoom=4)
    return m

```

## 📄 License

This repository is open-source and available under the MIT License.