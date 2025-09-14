import frappe
from frappe import _

def after_install():
    """Create default Weather Settings (City=Riyadh) + a 'Weather' workspace with shortcuts."""
    # 1) Weather Settings (Single)
    if frappe.db.exists("DocType", "Weather Settings"):
        ws = frappe.get_single("Weather Settings")
        if not ws.city:
            ws.city = "Riyadh"
        ws.save(ignore_permissions=True)


    if not frappe.db.exists("Workspace", "Weather"):
        blocks = [
            {"type": "heading", "data": {"text": _("Weather")}},
            {"type": "shortcut", "label": _("Weather"), "link_type": "DocType", "link_to": "Weather"},
            {"type": "shortcut", "label": _("Weather Settings"), "link_type": "DocType", "link_to": "Weather Settings"},

            {"type": "html", "data": {"html": "<div id='weather-workspace-block' style='margin-top:8px;'></div>"}},
        ]
        doc = frappe.get_doc({
            "doctype": "Workspace",
            "label": "Weather",
            "public": 1,
            "hide_custom": 0,
            "content": frappe.as_json(blocks),  
        })
        doc.insert(ignore_permissions=True)
