import frappe
from datetime import datetime

print("=" * 60)
print("🔌 DCIM PLUS - COMPLETE SNMP POLLER (ALL DEVICES)")
print("=" * 60)

try:
    from pysnmp.hlapi import *
    SNMP_AVAILABLE = True
    print("✅ pysnmp available")
except ImportError:
    SNMP_AVAILABLE = False
    print("⚠️ pysnmp not installed. Install with: pip install pysnmp")

# =====================================================
# APC PowerNet-MIB OIDs (APC UPS + CRAC)
# =====================================================

APC_UPS_OIDS = {
    "load_percentage": "1.3.6.1.4.1.318.1.1.1.4.3.3.1.0",
    "battery_runtime": "1.3.6.1.4.1.318.1.1.1.2.2.3.0",
    "battery_charge": "1.3.6.1.4.1.318.1.1.1.2.3.1.0",
    "battery_temp": "1.3.6.1.4.1.318.1.1.1.2.3.2.0",
    "battery_status": "1.3.6.1.4.1.318.1.1.1.2.1.1.0",
    "input_voltage": "1.3.6.1.4.1.318.1.1.1.3.3.1.0",
    "output_voltage": "1.3.6.1.4.1.318.1.1.1.4.3.2.1.0",
    "ups_status": "1.3.6.1.4.1.318.1.1.1.1.1.1.0",
}

APC_CRAC_OIDS = {
    "supply_temp": "1.3.6.1.4.1.318.1.3.4.1.1.2",
    "return_temp": "1.3.6.1.4.1.318.1.3.4.1.1.3",
    "fan_speed": "1.3.6.1.4.1.318.1.3.4.1.1.4",
    "cooling_capacity": "1.3.6.1.4.1.318.1.3.4.1.1.5",
    "cool_demand": "1.3.6.1.4.1.318.1.3.4.1.1.6",
    "humidity": "1.3.6.1.4.1.318.1.3.4.1.1.7",
}

# =====================================================
# IETF RFC1628 MIB OIDs (For Gamatronic, Riello UPS)
# =====================================================

IETF_UPS_OIDS = {
    "load_percentage": "1.3.6.1.2.1.33.1.4.4.1.5.1",
    "battery_runtime": "1.3.6.1.2.1.33.1.2.3.0",
    "battery_charge": "1.3.6.1.2.1.33.1.2.4.0",
    "battery_status": "1.3.6.1.2.1.33.1.2.1.0",
    "battery_temp": "1.3.6.1.2.1.33.1.2.7.0",
    "input_voltage": "1.3.6.1.2.1.33.1.3.3.1.3.1",
    "input_frequency": "1.3.6.1.2.1.33.1.3.3.1.4.1",
    "output_voltage": "1.3.6.1.2.1.33.1.4.4.1.2.1",
    "ups_manufacturer": "1.3.6.1.2.1.33.1.1.1.0",
    "ups_model": "1.3.6.1.2.1.33.1.1.2.0",
}

# =====================================================
# Generator SNMP OIDs (Generic)
# =====================================================

GENERATOR_OIDS = {
    "fuel_level": "1.3.6.1.4.1.318.1.1.1.1.1.1.0",
    "runtime_hours": "1.3.6.1.4.1.318.1.1.1.1.1.2.0",
    "engine_status": "1.3.6.1.4.1.318.1.1.1.1.1.3.0",
    "output_power": "1.3.6.1.4.1.318.1.1.1.1.1.4.0",
    "engine_temp": "1.3.6.1.4.1.318.1.1.1.1.1.5.0",
}

# =====================================================
# Helper Functions
# =====================================================

def snmp_get(ip, oid, community="public", port=161):
    """Get single SNMP value"""
    if not SNMP_AVAILABLE:
        return None

    try:
        error_indication, error_status, error_index, var_binds = next(
            getCmd(SnmpEngine(),
                   CommunityData(community),
                   UdpTransportTarget((ip, port)),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid)))
        )

        if error_indication or error_status:
            return None

        for var_bind in var_binds:
            return str(var_bind[1])
    except Exception as e:
        return None

    return None


# =====================================================
# UPS Polling Functions
# =====================================================

@frappe.whitelist()
def poll_apc_ups(ups_name=None):
    """Poll APC UPS using PowerNet-MIB"""
    results = []

    if ups_name:
        ups_list = [frappe.get_doc("UPS", ups_name)]
    else:
        ups_list = frappe.get_all("UPS", 
            filters={"snmp_host": ["!=", None], "ups_mib_type": "PowerNet (APC)"},
            fields=["name", "ups_name", "snmp_host", "snmp_community"])
        ups_list = [frappe.get_doc("UPS", u.name) for u in ups_list]

    for ups in ups_list:
        if not hasattr(ups, 'snmp_host') or not ups.snmp_host:
            continue

        print(f"📡 Polling APC UPS: {ups.ups_name} at {ups.snmp_host}...")

        data = {}
        for metric, oid in APC_UPS_OIDS.items():
            value = snmp_get(ups.snmp_host, oid, getattr(ups, 'snmp_community', 'public'))
            if value:
                data[metric] = value

        if data:
            try:
                if "load_percentage" in data:
                    ups.load_percentage = float(data["load_percentage"])
                if "battery_runtime" in data:
                    ups.runtime = int(float(data["battery_runtime"]))
                if "battery_charge" in data:
                    ups.battery_charge = float(data["battery_charge"])
                if "battery_temp" in data:
                    ups.battery_temp = float(data["battery_temp"])
                if "input_voltage" in data:
                    ups.input_voltage = float(data["input_voltage"])
                if "output_voltage" in data:
                    ups.output_voltage = float(data["output_voltage"])

                if "battery_status" in data:
                    status_map = {"1": "Good", "2": "Warning", "3": "Critical", "4": "Unknown"}
                    ups.battery_status = status_map.get(data["battery_status"], "Unknown")

                ups.last_snmp_poll = datetime.now()
                ups.save()
                print(f"   ✅ {ups.ups_name} - Load: {ups.load_percentage}%")
                results.append({"name": ups.ups_name, "status": "success", "data": data})
            except Exception as e:
                print(f"   ❌ Error: {e}")
                results.append({"name": ups.ups_name, "status": "error", "error": str(e)})
        else:
            print(f"   ⚠️ No data from {ups.ups_name}")
            results.append({"name": ups.ups_name, "status": "no_data"})

    return results


@frappe.whitelist()
def poll_ietf_ups(ups_name=None):
    """Poll UPS using standard IETF RFC1628 MIB (Gamatronic, Riello)"""
    results = []

    if ups_name:
        ups_list = [frappe.get_doc("UPS", ups_name)]
    else:
        ups_list = frappe.get_all("UPS", 
            filters={"snmp_host": ["!=", None], "ups_mib_type": ["in", ["RFC1628 (Standard)", "IETF"]]},
            fields=["name", "ups_name", "snmp_host", "snmp_community"])
        ups_list = [frappe.get_doc("UPS", u.name) for u in ups_list]

    for ups in ups_list:
        if not hasattr(ups, 'snmp_host') or not ups.snmp_host:
            continue

        print(f"📡 Polling IETF UPS: {ups.ups_name} at {ups.snmp_host}...")

        data = {}
        for metric, oid in IETF_UPS_OIDS.items():
            value = snmp_get(ups.snmp_host, oid, getattr(ups, 'snmp_community', 'public'))
            if value:
                data[metric] = value

        if data:
            try:
                if "load_percentage" in data:
                    ups.load_percentage = float(data["load_percentage"])
                if "battery_runtime" in data:
                    ups.runtime = int(float(data["battery_runtime"]))
                if "battery_charge" in data:
                    ups.battery_charge = float(data["battery_charge"])
                if "input_voltage" in data:
                    ups.input_voltage = float(data["input_voltage"])
                if "output_voltage" in data:
                    ups.output_voltage = float(data["output_voltage"])

                if "battery_status" in data:
                    status_map = {"1": "Good", "2": "Warning", "3": "Critical", "4": "Unknown"}
                    ups.battery_status = status_map.get(data["battery_status"], "Unknown")

                ups.last_snmp_poll = datetime.now()
                ups.save()
                print(f"   ✅ {ups.ups_name} - Load: {ups.load_percentage}%")
                results.append({"name": ups.ups_name, "status": "success", "data": data})
            except Exception as e:
                print(f"   ❌ Error: {e}")
                results.append({"name": ups.ups_name, "status": "error", "error": str(e)})
        else:
            print(f"   ⚠️ No data from {ups.ups_name}")
            results.append({"name": ups.ups_name, "status": "no_data"})

    return results


# =====================================================
# CRAC Unit Polling Functions
# =====================================================

@frappe.whitelist()
def poll_apc_crac(crac_name=None):
    """Poll APC CRAC units"""
    results = []

    if crac_name:
        crac_list = [frappe.get_doc("CRAC Unit", crac_name)]
    else:
        crac_list = frappe.get_all("CRAC Unit", 
            filters={"snmp_host": ["!=", None]},
            fields=["name", "unit_name", "snmp_host", "snmp_community"])
        crac_list = [frappe.get_doc("CRAC Unit", c.name) for c in crac_list]

    for crac in crac_list:
        if not hasattr(crac, 'snmp_host') or not crac.snmp_host:
            continue

        print(f"📡 Polling CRAC: {crac.unit_name} at {crac.snmp_host}...")

        data = {}
        for metric, oid in APC_CRAC_OIDS.items():
            value = snmp_get(crac.snmp_host, oid, getattr(crac, 'snmp_community', 'public'))
            if value:
                data[metric] = value

        if data:
            try:
                if "supply_temp" in data:
                    crac.supply_temp = float(data["supply_temp"])
                if "return_temp" in data:
                    crac.return_temp = float(data["return_temp"])
                if "fan_speed" in data:
                    crac.fan_speed = float(data["fan_speed"])
                if "cooling_capacity" in data:
                    crac.cooling_capacity = float(data["cooling_capacity"])
                if "humidity" in data:
                    crac.humidity = float(data["humidity"])

                crac.last_snmp_poll = datetime.now()
                crac.save()

                delta = crac.return_temp - crac.supply_temp if hasattr(crac, 'return_temp') and hasattr(crac, 'supply_temp') else 0
                print(f"   ✅ {crac.unit_name} - Supply: {crac.supply_temp}°C | Delta: {delta:.1f}°C")
                results.append({"name": crac.unit_name, "status": "success", "data": data})
            except Exception as e:
                print(f"   ❌ Error: {e}")
                results.append({"name": crac.unit_name, "status": "error", "error": str(e)})
        else:
            print(f"   ⚠️ No data from {crac.unit_name}")
            results.append({"name": crac.unit_name, "status": "no_data"})

    return results


# =====================================================
# Generator Polling Functions
# =====================================================

@frappe.whitelist()
def poll_generators():
    """Poll SNMP-enabled generators"""
    results = []

    generators = frappe.get_all("Generator", 
        filters={"snmp_host": ["!=", None]},
        fields=["name", "generator_name", "snmp_host", "snmp_community"])

    for gen in generators:
        if not gen.snmp_host:
            continue

        print(f"📡 Polling Generator: {gen.generator_name} at {gen.snmp_host}...")

        data = {}
        for metric, oid in GENERATOR_OIDS.items():
            value = snmp_get(gen.snmp_host, oid, gen.snmp_community or 'public')
            if value:
                data[metric] = value

        if data:
            try:
                doc = frappe.get_doc("Generator", gen.name)

                if "fuel_level" in data:
                    doc.fuel_level = float(data["fuel_level"])
                if "runtime_hours" in data:
                    doc.runtime_hours = float(data["runtime_hours"])
                if "engine_temp" in data:
                    doc.engine_temp = float(data["engine_temp"])

                doc.last_snmp_poll = datetime.now()
                doc.save()
                print(f"   ✅ {gen.generator_name} - Fuel: {doc.fuel_level}%")
                results.append({"name": gen.generator_name, "status": "success", "data": data})
            except Exception as e:
                print(f"   ❌ Error: {e}")
                results.append({"name": gen.generator_name, "status": "error", "error": str(e)})
        else:
            print(f"   ⚠️ No data from {gen.generator_name}")
            results.append({"name": gen.generator_name, "status": "no_data"})

    return results


# =====================================================
# Master Poll Function
# =====================================================

@frappe.whitelist()
def poll_all():
    """Poll ALL SNMP-enabled devices"""
    print("
" + "=" * 60)
    print("🔌 Starting COMPLETE SNMP Polling...")
    print("=" * 60)

    apc_results = poll_apc_ups()
    ietf_results = poll_ietf_ups()
    crac_results = poll_apc_crac()
    gen_results = poll_generators()

    print("
" + "=" * 60)
    print("📊 Polling Summary:")
    print(f"   APC UPS: {len([r for r in apc_results if r['status'] == 'success'])} succeeded")
    print(f"   IETF UPS: {len([r for r in ietf_results if r['status'] == 'success'])} succeeded")
    print(f"   CRAC: {len([r for r in crac_results if r['status'] == 'success'])} succeeded")
    print(f"   Generators: {len([r for r in gen_results if r['status'] == 'success'])} succeeded")
    print("=" * 60)

    return {
        "apc_ups": apc_results,
        "ietf_ups": ietf_results,
        "crac": crac_results,
        "generators": gen_results
    }


@frappe.whitelist()
def test_connection(ip, community="public"):
    """Test SNMP connection to a device"""
    result = snmp_get(ip, "1.3.6.1.2.1.1.1.0", community)
    if result:
        return {"status": "success", "sysDescr": result}
    return {"status": "error", "message": "No response from device"}

print("\n✅ SNMP Poller API loaded successfully!")
