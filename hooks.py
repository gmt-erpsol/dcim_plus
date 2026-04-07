app_name = "dcim_plus"
app_title = "Dcim Plus"
app_publisher = "gemtad"
app_description = "Data center Infrastructure Management Monitoring And control"
app_email = "gamtadabala@gmail.com"
app_license = "mit"

# Apps
# ------------------

# Website context
website_context = {
    "brand_html": "DCIM PLUS"
}

# API endpoints
website_route_rules = [
    {"from_route": "/api/method/dcim_plus.api.dr_api.save_dr_plan",
     "to_route": "/api/method/dcim_plus.api.dr_api.save_dr_plan"}
]

# Custom login page
login_page = "login"
# Custom UI Shell
home_page = "dcim"
web_include_css = ["/assets/dcim_plus/css/app.css"]
web_include_js = ["/assets/dcim_plus/js/app.js"]

# DCIM Plus Custom UI

# Custom UI Shell
home_page = "dcim"
web_include_css = ["/assets/dcim_plus/css/app.css"]
web_include_js = ["/assets/dcim_plus/js/app.js"]
