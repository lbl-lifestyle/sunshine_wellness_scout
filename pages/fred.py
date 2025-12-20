import streamlit as st
import requests
from openai import OpenAI

# Secrets
XAI_API_KEY = st.secrets["XAI_API_KEY"]
RESEND_API_KEY = st.secrets["RESEND_API_KEY"]
YOUR_EMAIL = st.secrets["YOUR_EMAIL"]
PEXELS_API_KEY = st.secrets.get("PEXELS_API_KEY", "")

client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
MODEL_NAME = "grok-4-1-fast-reasoning"

def fetch_pexels_image(neighborhood, location_hint="", fallback_city=""):
    """Fetch one relevant, high-quality image — smart query to avoid duplicates/wrong city"""
    if not PEXELS_API_KEY:
        return None

    headers = {"Authorization": PEXELS_API_KEY}
    base_url = "https://api.pexels.com/v1/search"

    # Primary query: neighborhood + location
    queries = []
    if neighborhood and location_hint:
        queries.append(f"{neighborhood} {location_hint} neighborhood homes landscape nature")
    if neighborhood:
        queries.append(f"{neighborhood} suburb residential area homes")
    if fallback_city:
        queries.append(f"{fallback_city} neighborhood aerial view homes nature")

    for query in queries:
        params = {
            "query": query,
            "per_page": 5,  # Get a few to choose from
            "orientation": "landscape"
        }
        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                photos = data.get("photos", [])
                if photos:
                    # Return the first high-quality, unique-looking photo
                    return photos[0]["src"]["large2x"]
        except:
            continue
    return None

def add_images_to_report(report_text, location_hint=""):
    """Insert one accurate photo under each Top 5 neighborhood"""
    lines = report_text.split('\n')
    enhanced_lines = []
    in_top_5 = False

    for line in lines:
        enhanced_lines.append(line)

        if "Top 5 Neighborhoods" in line or "Top 5 Suburbs" in line:
            in_top_5 = True

        if in_top_5 and line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
            parts = line.split('-', 1)
            if len(parts) > 1:
                name_part = parts[0].strip()[2:].strip()  # e.g., "West Asheville"
                img_url = fetch_pexels_image(name_part, location_hint, location_hint or "USA")
                if img_url:
                    enhanced_lines.append("")
                    enhanced_lines.append(f"![{name_part} – Scenic homes and neighborhood view]({img_url})")
                    enhanced_lines.append("")

    return '\n'.join(enhanced_lines)

# ... (rest of show() function is the same as before, just replace the add_images_to_report and fetch functions)

# Inside the report generation block:
location_hint = location.strip() or "wellness community USA"

# After generating displayed_report and full_report:
displayed_report_with_images = add_images_to_report(displayed_report, location_hint)
full_report_with_images = add_images_to_report(full_report, location_hint)

# Then use displayed_report_with_images for st.markdown and full_report_with_images for email/history
