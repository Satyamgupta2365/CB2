import requests
from PIL import Image
from io import BytesIO
import json

# 🔐 Your Sentinel Hub credentials
CLIENT_ID = "edc27bf9-639a-45e8-9745-88e4ffc5f174"
CLIENT_SECRET = "inrHG7CE8evWZlKxy0B6n7aJ5Aq33Lem"

# 📍 Get bounding box coordinates from user
print("🌍 TROPICAL SATELLITE IMAGE FETCHER")
print("=" * 50)
print("\nEnter the 4 coordinates for your area:")
print()

min_lon = float(input("⿡  Minimum Longitude (min_lon): "))
min_lat = float(input("⿢  Minimum Latitude (min_lat): "))
max_lon = float(input("⿣  Maximum Longitude (max_lon): "))
max_lat = float(input("⿤  Maximum Latitude (max_lat): "))

BBOX = [min_lon, min_lat, max_lon, max_lat]
print(f"\n✅ Bounding box set to: {BBOX}")

# 🔑 Get access token
token_url = "https://services.sentinel-hub.com/oauth/token"
data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}
response = requests.post(token_url, data=data)
access_token = response.json()["access_token"]
print("✅ Authentication successful")

# 🛰 Request true-color Sentinel-2 image
process_url = "https://services.sentinel-hub.com/api/v1/process"

payload = {
    "input": {
        "bounds": {
            "bbox": BBOX,
            "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"}
        },
        "data": [{
            "type": "sentinel-2-l2a",
            "dataFilter": {
                "timeRange": {
                    "from": "2024-12-01T00:00:00Z",
                    "to": "2025-01-31T23:59:59Z"
                },
                "maxCloudCoverage": 20
            }
        }]
    },
    "output": {
        "width": 1024,
        "height": 1024,
        "responses": [{
            "identifier": "default",
            "format": {"type": "image/png"}
        }]
    },
    "evalscript": """
    //VERSION=3
    function setup() {
        return {
            input: ["B04", "B03", "B02", "dataMask"],
            output: { bands: 4 }
        };
    }

    function evaluatePixel(sample) {
        // True color RGB with enhanced green for tropical vegetation
        let gain = 3.0;
        return [
            sample.B04 * gain,      // Red
            sample.B03 * gain * 1.1, // Green (boosted for lush vegetation)
            sample.B02 * gain * 0.9, // Blue (slightly reduced)
            sample.dataMask
        ];
    }
    """
}

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

print("🛰 Fetching Sentinel-2 true-color image...")
res = requests.post(process_url, headers=headers, json=payload)

if res.status_code == 200:
    img = Image.open(BytesIO(res.content))
    img.save("true_color_sentinel.png")
    print("✅ True-color satellite image saved as 'true_color_sentinel.png'")
    img.show()
else:
    print(f"❌ Error {res.status_code}: {res.text}")
    print("\n💡 Troubleshooting tips:")
    print("1. Check if your credentials are valid")
    print("2. Verify the bounding box coordinates")
    print("3. Try adjusting the date range")
    print("4. Check cloud coverage settings")
