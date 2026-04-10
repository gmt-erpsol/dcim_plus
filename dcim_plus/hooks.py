app_name = "dcim_plus"
app_title = "Dcim Plus"
app_publisher = "gemtad"
app_description = "Data center Infrastructure Management Monitoring And control"
app_email = "gamtadabala@gmail.com"
app_license = "mit"
# In dcim_plus/hooks.py

# Add this to your hooks.py file

# Custom login page
login_page = "login"
# Override website context
website_context = {
    "login_page": "login"
}
# API endpoints
# API endpoints
website_route_rules = [
    {"from_route": "/api/method/dcim_plus.api.dr_api.save_dr_plan",
     "to_route": "/api/method/dcim_plus.api.dr_api.save_dr_plan"}
] 

website_route_rules = [
    {"from_route": "/", "to_route": "index"}
]
# Correct format for website_route_rules

# Add at the bottom]
# Critical: Redirect EVERYTHING to your UI
# Add at the bottom
# Remove website_route_rules for now
# Just keep:
home_page = "index"
# Custom CSS/JS for Frappe Desk
app_include_css = "/assets/dcim_plus/css/dcim_custom.css"
app_include_js = "/assets/dcim_plus/js/dcim_custom.js"
