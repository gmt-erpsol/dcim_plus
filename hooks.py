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

# ============================================
# DCIM PLUS - CUSTOM UI
# ============================================

app_include_css = "dcim_theme.css"
app_include_js = "dcim_ui.js"
