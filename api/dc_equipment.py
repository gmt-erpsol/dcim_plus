
import frappe
import json

@frappe.whitelist(allow_guest=False)
def get_equipment():
    """Get all DC equipment"""
    try:
        equipment = frappe.get_all("DC Equipment", 
            fields=["equipment_name", "equipment_type", "x_position", "z_position"])
        return equipment
    except Exception as e:
        return []

@frappe.whitelist(allow_guest=False)
def save_layout():
    """Save DC equipment layout"""
    try:
        data = frappe.local.form_dict
        objects = json.loads(data.get("objects", "[]"))
        
        # Clear existing
        frappe.db.sql("DELETE FROM `tabDC Equipment`")
        
        # Save new
        for obj in objects:
            doc = frappe.get_doc({
                "doctype": "DC Equipment",
                "equipment_name": obj["equipment_name"],
                "equipment_type": obj["equipment_type"],
                "x_position": obj["x_position"],
                "z_position": obj["z_position"]
            })
            doc.insert()
        
        frappe.db.commit()
        return {"success": True, "count": len(objects)}
    except Exception as e:
        return {"success": False, "error": str(e)}
