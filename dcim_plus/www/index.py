from __future__ import unicode_literals
import frappe

def get_context(context):
    # Redirect to your static HTML page
    frappe.local.response["type"] = "redirect"
    frappe.local.response["location"] = "/assets/dcim_plus/index.html"
    return context
