from __future__ import unicode_literals
import frappe

def get_context(context):
    if frappe.session.user != "Guest":
        frappe.local.flags.redirect_location = "/index"
        raise frappe.Redirect
