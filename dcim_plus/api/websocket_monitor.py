# dcim_plus/api/websocket_monitor.py

import frappe
import json
from frappe.utils import now
from datetime import datetime

class RealTimeMonitor:
    """WebSocket-based real-time monitoring"""
    
    @staticmethod
    def get_live_data():
        """Get current snapshot for WebSocket push"""
        return {
            "timestamp": now(),
            "cooling": get_realtime_cooling_data(),
            "power": get_realtime_power_data(),
            "alerts": get_realtime_alert_count()
        }


def get_realtime_cooling_data():
    """Get current cooling metrics"""
    cracs = frappe.get_all("CRAC Unit",
        fields=["unit_name", "supply_temp", "return_temp", "fan_speed", "status"])
    
    return [{
        "name": c.unit_name,
        "temp": c.supply_temp,
        "delta": round((c.return_temp - c.supply_temp), 1) if c.return_temp else 0,
        "fan": c.fan_speed,
        "status": c.status
    } for c in cracs]


def get_realtime_power_data():
    """Get current power metrics"""
    ups_list = frappe.get_all("UPS", fields=["ups_name", "load_percentage", "battery_status"])
    generators = frappe.get_all("Generator", fields=["generator_name", "fuel_level"])
    
    return {
        "ups": [{"name": u.ups_name, "load": u.load_percentage, "battery": u.battery_status} for u in ups_list],
        "generators": [{"name": g.generator_name, "fuel": g.fuel_level} for g in generators]
    }


def get_realtime_alert_count():
    """Get current alert counts"""
    return frappe.db.count("Alarm Log", filters={"status": "Active"})
