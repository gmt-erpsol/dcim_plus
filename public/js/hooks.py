
# =====================================================
# DCIM PLUS - Custom UI/UX (Corrected Paths)
# =====================================================

# Add custom CSS (note: no leading slash)
app_include_css = [
    "dcim_custom.css"
]

# Add custom JS
app_include_js = [
    "dcim_custom.js"
]

# Website context for footer
website_context = {
    "brand_html": "<div class='dcim-brand'>🏭 DCIM PLUS</div>",
    "copyright": "Awash Main Data Center",
    "footer_powered": "Powered by DCIM PLUS"
}

# Custom CSS and JS
app_include_css = ["css/dcim_custom.css"]
app_include_js = ["js/dcim_custom.js"]

# Redirect to custom UI
def redirect_to_custom_ui():
    from frappe import _
    if frappe.session.user != "Guest":
        if frappe.request.path == "/" or frappe.request.path == "/app":
            frappe.local.flags.redirect_location = "/dcim"
            raise frappe.Redirect

on_app_ready = [redirect_to_custom_ui]
