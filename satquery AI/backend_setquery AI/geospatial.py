import rasterio

def extract_metadata(file_path: str):
    """Extracts bounds and coordinate reference system from a GeoTIFF."""
    try:
        with rasterio.open(file_path) as src:
            bounds = src.bounds
            crs = str(src.crs)
            res = src.res
            return {
                "success": True,
                "bounds": {"left": bounds.left, "bottom": bounds.bottom, "right": bounds.right, "top": bounds.top},
                "crs": crs,
                "resolution": res
            }
    except Exception as e:
        return {"success": False, "error": str(e)}