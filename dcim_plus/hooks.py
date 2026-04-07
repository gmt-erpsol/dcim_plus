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
# Correct format for website_route_rules

# Add at the bottom]
# Critical: Redirect EVERYTHING to your UI
home_page = "dcim"
