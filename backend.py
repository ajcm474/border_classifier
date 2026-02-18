import time
import urllib

from .config import NOMINATIM_URL, API_RATE_LIMIT, USER_AGENT


LAST_REQUEST_TIME = time.time()


def query_osm_boundary(name: str):
    global LAST_REQUEST_TIME
    params={
        "q": name,
        "format": "json",
        "addressdetails": 1,
        "limit": 10,
        "polygon_geojson": 0,
    }
    url = f"{NOMINATIM_URL}?{urllib.parse.urlencode(params)}"
    now = time.time()
    wait = API_RATE_LIMIT - (now - LAST_REQUEST_TIME)
    if wait > 0:
        time.sleep(wait)
    LAST_REQUEST_TIME = time.time()
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": USER_AGENT, "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except Exception as exc:
        raise RuntimeError(f"Nominatim request failed: {exc}") from exc