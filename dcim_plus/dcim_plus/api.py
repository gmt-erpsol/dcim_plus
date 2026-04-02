import frappe

@frappe.whitelist()
def get_heatmap_data():
    """Return data for Live Power & Thermal Heatmap"""
    try:
        racks = frappe.get_all("Rack",
            fields=["name as rack_name", "room", "used_u", "rack_height"],
            filters={"status": ["!=", "Maintenance"]},
            order_by="name"
        )

        data = []
        for rack in racks:
            # Get latest temperature
            temp = frappe.get_all("Temperature Sensor",
                fields=["temperature"],
                filters={"rack": rack.name},
                order_by="last_reading desc",
                limit=1
            )
            temperature = temp[0].temperature if temp else 22.0

            # Get power load from PDU
            pdu = frappe.get_all("PDU",
                fields=["load_percentage"],
                filters={"rack": rack.name},
                limit=1
            )
            load_percentage = pdu[0].load_percentage if pdu else 45.0

            data.append({
                "rack_name": rack.rack_name,
                "temperature": round(temperature, 1),
                "load_percentage": round(load_percentage, 1),
                "room_name": rack.room
            })

        return data

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Heatmap Data Error")
        return []
