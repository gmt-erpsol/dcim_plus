from __future__ import unicode_literals
import frappe

def get_context(context):
    context.no_cache = 1
    context.show_sidebar = True
    
    # Pass user info to template
    context.user = frappe.session.user
    context.full_name = frappe.db.get_value("User", frappe.session.user, "full_name")
    
    return context
