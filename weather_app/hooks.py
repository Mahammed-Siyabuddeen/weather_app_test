from . import __version__ as app_version

app_name = "weather_app"
app_title = "Weather App"
app_publisher = "Eslam Ashraf"
app_description = "weather_app"
app_icon = "octicon octicon-sun"
app_color = "grey"
app_email = "esalam@gmail.com"
app_license = "gpl-2.0"

required_apps = ["erpnext"]

# UI bottom bar
app_include_js = "/assets/weather_app/js/weather_bar.js"

# app_include_css = "/assets/weather_app/css/weather_bar.css"


scheduler_events = {
    "cron": {
        "*/5 * * * *": [
            "weather_app.tasks.update_weather"
        ]
    }
}
