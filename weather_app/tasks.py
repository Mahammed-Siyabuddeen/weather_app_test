import frappe
from frappe.utils import now_datetime
from .api import _get_settings, _fetch_from_openweather

def update_weather():

    api_key, default_city = _get_settings()
    cities = frappe.get_all("Weather", pluck="name") or [default_city]
    updated = 0
    for city in set(cities):
        try:
            data = _fetch_from_openweather(city, api_key)
        except Exception:
            frappe.log_error(frappe.get_traceback(), f"Weather update failed for {city}")
            continue

        name = frappe.db.exists("Weather", city) or frappe.db.get_value("Weather", {"city": city}, "name")
        if name:
            doc = frappe.get_doc("Weather", name)
        else:
            doc = frappe.new_doc("Weather")
            doc.city = city


        changed = (doc.temperature != data["temperature"]) or (doc.humidity != data["humidity"])
        doc.temperature = data["temperature"]
        doc.humidity = data["humidity"]
        doc.last_updated_on = now_datetime()
        doc.save(ignore_permissions=True)
        if changed:
            updated += 1

    frappe.db.commit()
    return {"updated": updated, "cities": cities}
