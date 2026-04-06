import frappe
import json

@frappe.whitelist()
def get_data_center_3d_data():
    """Fetch all data for 3D visualization"""
    
    result = {
        "data_centers": [],
        "rooms": [],
        "racks": [],
        "devices": [],
        "power_equipment": [],
        "cooling_equipment": [],
        "fire_equipment": []
    }
    
    # Get Data Centers
    data_centers = frappe.get_all("Data Center", 
        fields=["name", "data_center_name", "status"])
    result["data_centers"] = data_centers
    
    # Get Rooms
    rooms = frappe.get_all("Room",
        fields=["name", "room_name", "room_type", "data_center", "width", "depth"])
    result["rooms"] = rooms
    
    # Get Racks
    racks = frappe.get_all("Rack",
        fields=["name", "rack_name", "room", "rack_height", "position_x", "position_z", 
                "current_load", "current_temp", "status"])
    result["racks"] = racks
    
    # Get IT Assets
    devices = frappe.get_all("IT Asset",
        fields=["name", "asset_name", "asset_type", "rack", "position_u", "height_u",
                "status", "temperature", "power_rating", "manufacturer", "model"])
    result["devices"] = devices
    
    # Get Power Equipment (UPS)
    ups_list = frappe.get_all("UPS",
        fields=["name", "ups_name", "status", "load_percentage", "capacity_kva"])
    for ups in ups_list:
        result["power_equipment"].append({
            "type": "ups",
            "name": ups.ups_name,
            "status": ups.status,
            "load": ups.load_percentage,
            "capacity": ups.capacity_kva
        })
    
    # Get PDU
    pdu_list = frappe.get_all("PDU",
        fields=["name", "pdu_name", "pdu_type", "status", "utilization"])
    for pdu in pdu_list:
        result["power_equipment"].append({
            "type": "pdu",
            "name": pdu.pdu_name,
            "pdu_type": pdu.pdu_type,
            "status": pdu.status,
            "load": pdu.utilization
        })
    
    # Get Generator
    gen_list = frappe.get_all("Generator",
        fields=["name", "generator_name", "status", "capacity_kw", "fuel_level"])
    for gen in gen_list:
        result["power_equipment"].append({
            "type": "generator",
            "name": gen.generator_name,
            "status": gen.status,
            "capacity": gen.capacity_kw,
            "fuel_level": gen.fuel_level
        })
    
    # Get CRAC Units
    crac_list = frappe.get_all("CRAC Unit",
        fields=["name", "unit_name", "status", "cooling_capacity", "supply_temp"])
    for crac in crac_list:
        result["cooling_equipment"].append({
            "type": "crac",
            "name": crac.unit_name,
            "status": crac.status,
            "capacity": crac.cooling_capacity,
            "temp": crac.supply_temp
        })
    
    # Get Fire Systems
    fire_list = frappe.get_all("Fire System",
        fields=["name", "system_name", "system_type", "agent_type", "status", "pressure"])
    for fire in fire_list:
        result["fire_equipment"].append({
            "type": "fire",
            "name": fire.system_name,
            "system_type": fire.system_type,
            "status": fire.status,
            "pressure": fire.pressure
        })
    
    return result

@frappe.whitelist()
def get_device_details(device_name):
    """Get detailed information for a specific device"""
    device = frappe.get_doc("IT Asset", device_name)
    return {
        "name": device.name,
        "asset_name": device.asset_name,
        "asset_type": device.asset_type,
        "manufacturer": device.manufacturer,
        "model": device.model,
        "serial_number": device.serial_number,
        "status": device.status,
        "temperature": device.temperature,
        "power_rating": device.power_rating,
        "ip_address": device.ip_address,
        "purchase_date": str(device.purchase_date) if device.purchase_date else None
    }
