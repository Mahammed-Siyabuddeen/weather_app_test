import frappe
import requests
from frappe.utils import now_datetime

def _get_settings():
 
    api_key = None
    default_city = "Riyadh"
    try:
        api_key = frappe.db.get_single_value("Weather Settings", "api_key")
        dc = frappe.db.get_single_value("Weather Settings", "default_city")
        if dc:
            default_city = dc
    except Exception:
        pass
    return api_key, default_city

def _fetch_from_openweather(city: str, api_key: str) -> dict:
    
    if not api_key:
        raise frappe.ValidationError("OpenWeather API key is missing. Set it in Weather Settings.")
    params = {"q": city, "appid": api_key, "units": "metric"}
    r = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params, timeout=15)
    r.raise_for_status()
    j = r.json() or {}
    main = j.get("main") or {}
    temp = float(main.get("temp"))
    humidity = float(main.get("humidity"))
    return {
        "city": city,
        "temperature": temp,
        "humidity": humidity,
        "last_updated_on": now_datetime(),
    }

@frappe.whitelist()
def get_latest(city: str | None = None):

    _, default_city = _get_settings()
    target = (city or default_city or "Riyadh").strip()
    name = frappe.db.exists("Weather", target) or frappe.db.get_value("Weather", {"city": target}, "name")
    if not name:
        return {}
    d = frappe.get_doc("Weather", name)
    return {
        "city": d.city,
        "temperature": d.temperature,
        "humidity": d.humidity,
        "last_updated_on": d.last_updated_on,
    }
