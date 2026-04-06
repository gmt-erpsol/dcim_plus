import frappe
import json

@frappe.whitelist()
def save_design(design_name, design_data):
    """Save a 3D design to the database"""
    
    # Check if design already exists
    existing = frappe.db.exists("DCIM 3D Design", {"design_name": design_name})
    
    if existing:
        # Update existing
        doc = frappe.get_doc("DCIM 3D Design", existing)
        doc.design_data = json.dumps(design_data)
        doc.save()
    else:
        # Create new
        doc = frappe.get_doc({
            "doctype": "DCIM 3D Design",
            "design_name": design_name,
            "design_data": json.dumps(design_data)
        })
        doc.insert()
    
    frappe.db.commit()
    return {"success": True, "name": doc.name}

@frappe.whitelist()
def load_design(design_name):
    """Load a saved design"""
    doc = frappe.get_doc("DCIM 3D Design", {"design_name": design_name})
    return json.loads(doc.design_data)

@frappe.whitelist()
def list_designs():
    """List all saved designs"""
    designs = frappe.get_all("DCIM 3D Design", fields=["name", "design_name", "modified"])
    return designs

@frappe.whitelist()
def delete_design(design_name):
    """Delete a design"""
    doc = frappe.get_doc("DCIM 3D Design", {"design_name": design_name})
    doc.delete()
    frappe.db.commit()
    return {"success": True}
