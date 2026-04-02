import frappe

@frappe.whitelist()
def save_dr_plan(plan_name, plan_type, severity, rto_target):
    """Save Disaster Recovery Plan"""
    try:
        dr_plan = frappe.get_doc({
            "doctype": "Disaster Recovery Plan",
            "plan_name": plan_name,
            "plan_type": plan_type,
            "severity": severity,
            "rto_target": int(rto_target),
            "status": "Active"
        })
        dr_plan.insert()
        frappe.db.commit()
        
        return {
            "success": True,
            "message": f"DR Plan '{plan_name}' created successfully"
        }
    except Exception as e:
        frappe.db.rollback()
        return {
            "success": False,
            "message": str(e)
        }
