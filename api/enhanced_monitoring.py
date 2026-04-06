import frappe
from frappe.utils import now
from datetime import datetime, timedelta

@frappe.whitelist(allow_guest=False)
def get_complete_monitoring_data():
    """Get ALL monitoring data - one API to rule them all"""
    
    response = {
        "timestamp": now(),
        "status": "success",
        "data": {
            "cooling": get_cooling_data(),
            "power": get_power_data(),
            "environmental": get_environmental_data(),
            "alerts": get_active_alerts(),
            "efficiency": get_efficiency_metrics()
        }
    }
    
    return response


def get_cooling_data():
    """Get all CRAC unit data"""
    cracs = frappe.get_all("CRAC Unit",
        fields=["unit_name", "zone", "supply_temp", "return_temp", "cooling_capacity", 
                "fan_speed", "status", "power_usage", "humidity"])
    
    cooling_data = []
    total_capacity = 0
    total_power = 0
    
    for crac in cracs:
        delta_t = (crac.return_temp - crac.supply_temp) if crac.return_temp and crac.supply_temp else 0
        efficiency = (crac.cooling_capacity / crac.power_usage * 100) if crac.power_usage else 0
        
        cooling_data.append({
            "name": crac.unit_name,
            "zone": crac.zone,
            "supply_temp": crac.supply_temp or 0,
            "return_temp": crac.return_temp or 0,
            "delta_t": round(delta_t, 1),
            "cooling_capacity_kw": crac.cooling_capacity or 0,
            "fan_speed_percent": crac.fan_speed or 0,
            "power_usage_kw": crac.power_usage or 0,
            "efficiency_percent": round(efficiency, 1),
            "humidity_percent": crac.humidity or 0,
            "status": crac.status or "Running",
            "performance": "Good" if delta_t > 8 else "Warning" if delta_t > 5 else "Critical"
        })
        
        total_capacity += crac.cooling_capacity or 0
        total_power += crac.power_usage or 0
    
    return {
        "units": cooling_data,
        "total_cooling_capacity_kw": total_capacity,
        "total_power_usage_kw": total_power,
        "average_efficiency": round((total_capacity / total_power * 100) if total_power else 0, 1),
        "hot_spots": []
    }


def get_power_data():
    """Get comprehensive power data"""
    
    # UPS data
    ups_units = frappe.get_all("UPS",
        fields=["ups_name", "capacity_kva", "load_percentage", "battery_status", 
                "input_voltage", "output_voltage", "runtime", "status"])
    
    ups_data = []
    total_ups_capacity = 0
    total_ups_load = 0
    
    for ups in ups_units:
        current_load = (ups.capacity_kva * ups.load_percentage / 100) if ups.capacity_kva else 0
        ups_data.append({
            "name": ups.ups_name,
            "capacity_kva": ups.capacity_kva or 0,
            "load_percent": ups.load_percentage or 0,
            "current_load_kw": round(current_load, 1),
            "battery_status": ups.battery_status or "Good",
            "input_voltage": ups.input_voltage or 0,
            "output_voltage": ups.output_voltage or 0,
            "runtime_minutes": ups.runtime or 0,
            "status": ups.status or "Normal",
            "health": "Good" if (ups.load_percentage or 0) < 70 and ups.battery_status == "Good" else "Warning"
        })
        total_ups_capacity += ups.capacity_kva or 0
        total_ups_load += current_load
    
    # Generator data
    generators = frappe.get_all("Generator",
        fields=["generator_name", "capacity_kw", "fuel_level", "runtime_hours", "status"])
    
    gen_data = []
    for gen in generators:
        gen_data.append({
            "name": gen.generator_name,
            "capacity_kw": gen.capacity_kw or 0,
            "fuel_level_percent": gen.fuel_level or 0,
            "runtime_hours": gen.runtime_hours or 0,
            "available_power_kw": (gen.capacity_kw * gen.fuel_level / 100) if gen.fuel_level else 0,
            "status": gen.status or "Ready",
            "health": "Good" if (gen.fuel_level or 0) > 20 else "Critical"
        })
    
    return {
        "ups": ups_data,
        "generators": gen_data,
        "summary": {
            "total_ups_capacity_kva": total_ups_capacity,
            "total_ups_load_kw": round(total_ups_load, 1),
            "total_generator_capacity_kw": sum(g["capacity_kw"] for g in gen_data),
            "available_backup_power_kw": round(sum(g["available_power_kw"] for g in gen_data), 1),
            "power_efficiency": round((total_ups_load / total_ups_capacity * 100) if total_ups_capacity else 0, 1)
        }
    }


def get_environmental_data():
    """Get environmental monitoring data"""
    
    # Temperature sensors
    temp_sensors = frappe.get_all("Temperature Sensor",
        fields=["sensor_name", "room", "rack", "temperature", "threshold", "status"])
    
    temp_data = []
    avg_temp = 0
    for sensor in temp_sensors:
        location = sensor.room or sensor.rack or "Unknown"
        temp_data.append({
            "name": sensor.sensor_name,
            "location": location,
            "temperature": sensor.temperature or 0,
            "threshold": sensor.threshold or 30,
            "status": sensor.status or "Normal",
            "risk": "High" if sensor.temperature and sensor.threshold and sensor.temperature > sensor.threshold else "Normal"
        })
        avg_temp += sensor.temperature or 0
    
    avg_temp = avg_temp / len(temp_sensors) if temp_sensors else 0
    
    # Calculate environmental score
    high_temps = len([t for t in temp_data if t.get("temperature", 0) > 25])
    environmental_score = max(0, 100 - (high_temps * 10))
    
    return {
        "temperature_sensors": temp_data,
        "average_temperature": round(avg_temp, 1),
        "environmental_score": environmental_score
    }


def get_active_alerts():
    """Get all active alerts"""
    alerts = frappe.get_all("Alarm Log",
        fields=["alarm_id", "alarm_type", "severity", "source", "description", "timestamp"],
        filters={"status": "Active"},
        order_by="timestamp desc",
        limit=20)
    
    return {
        "count": len(alerts),
        "critical": len([a for a in alerts if a.severity == "Critical"]),
        "high": len([a for a in alerts if a.severity == "High"]),
        "medium": len([a for a in alerts if a.severity == "Medium"]),
        "low": len([a for a in alerts if a.severity == "Low"]),
        "list": alerts
    }


def get_efficiency_metrics():
    """Calculate efficiency metrics"""
    
    # Calculate PUE (simplified)
    ups_list = frappe.get_all("UPS", fields=["capacity_kva", "load_percentage"])
    total_power = sum((u.capacity_kva * u.load_percentage / 100) for u in ups_list if u.capacity_kva and u.load_percentage)
    
    crac_list = frappe.get_all("CRAC Unit", fields=["power_usage"])
    cooling_power = sum(c.power_usage for c in crac_list if c.power_usage)
    
    pue = (total_power + cooling_power) / total_power if total_power > 0 else 1.5
    cooling_efficiency = round((cooling_power / total_power * 100) if total_power > 0 else 0, 1)
    power_efficiency = round((total_power / (total_power + cooling_power) * 100) if total_power > 0 else 0, 1)
    
    rating = "Excellent" if pue < 1.5 else "Good" if pue < 1.8 else "Needs Improvement"
    
    return {
        "pue": round(pue, 2),
        "cooling_efficiency": cooling_efficiency,
        "power_efficiency": power_efficiency,
        "rating": rating
    }
