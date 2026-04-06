import frappe
import json

@frappe.whitelist()
def save_design_to_db(design_name, objects_data, room_name=None):
    """Save 3D design to database"""
    try:
        objects = json.loads(objects_data)
        
        # Create or update design record
        if frappe.db.exists("ThreeD Design", design_name):
            design = frappe.get_doc("ThreeD Design", design_name)
        else:
            design = frappe.new_doc("ThreeD Design")
            design.design_name = design_name
        
        design.room = room_name
        design.design_data = json.dumps(objects)
        design.object_count = len(objects)
        design.save()
        
        frappe.db.commit()
        return {"success": True, "message": f"Design '{design_name}' saved"}
    except Exception as e:
        frappe.db.rollback()
        return {"success": False, "message": str(e)}

@frappe.whitelist()
def load_design_from_db(design_name):
    """Load a saved design from database"""
    try:
        if frappe.db.exists("ThreeD Design", design_name):
            design = frappe.get_doc("ThreeD Design", design_name)
            return {
                "success": True,
                "design_name": design.design_name,
                "room": design.room,
                "objects": json.loads(design.design_data) if design.design_data else [],
                "created": design.creation
            }
        return {"success": False, "message": "Design not found"}
    except Exception as e:
        return {"success": False, "message": str(e)}

@frappe.whitelist()
def list_designs():
    """List all saved 3D designs"""
    try:
        designs = frappe.get_all("ThreeD Design", 
                                 fields=["name", "design_name", "room", "object_count", "creation"], 
                                 order_by="creation desc")
        return designs
    except Exception as e:
        return []

@frappe.whitelist()
def delete_design(design_name):
    """Delete a saved design"""
    try:
        if frappe.db.exists("ThreeD Design", design_name):
            frappe.delete_doc("ThreeD Design", design_name)
            frappe.db.commit()
            return {"success": True}
        return {"success": False}
    except Exception as e:
        return {"success": False, "message": str(e)}
