from __future__ import unicode_literals
import frappe

def get_context(context):
    if frappe.session.user != "Guest":
        # Redirect to your custom dashboard after login
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/assets/dcim_plus/index.html"
        raise frappe.Redirect
