// DCIM Plus - Custom UI Enhancements

frappe.ready(function() {
    // Add custom CSS class to body
    $('body').addClass('dcim-plus-theme');
    
    // Custom dashboard widgets
    if (frappe.get_route()[0] === "dashboard") {
        addDcimWidgets();
    }
    
    // Real-time status updates for assets
    if (frappe.get_route()[0] === "Form" && frappe.get_route()[1] === "IT Asset") {
        startAssetStatusPolling();
    }
});

// Add DCIM specific widgets to dashboard
function addDcimWidgets() {
    // Add power capacity widget
    frappe.call({
        method: "dcim_theme.api.get_power_summary",
        callback: function(r) {
            if (r.message) {
                // Render power widget
                renderPowerWidget(r.message);
            }
        }
    });
    
    // Add temperature monitoring widget
    frappe.call({
        method: "dcim_theme.api.get_temperature_summary",
        callback: function(r) {
            if (r.message) {
                renderTemperatureWidget(r.message);
            }
        }
    });
}

// Real-time asset monitoring
function startAssetStatusPolling() {
    setInterval(function() {
        frappe.call({
            method: "dcim_theme.api.get_asset_status",
            args: {
                asset_name: frappe.get_route()[2]
            },
            callback: function(r) {
                if (r.message) {
                    updateAssetStatusIndicators(r.message);
                }
            }
        });
    }, 30000); // Update every 30 seconds
}

// Custom form buttons for DCIM operations
frappe.ui.form.on('IT Asset', {
    refresh: function(frm) {
        // Add custom buttons
        frm.add_custom_button(__('View Power Path'), function() {
            showPowerPathDiagram(frm.doc.name);
        });
        
        frm.add_custom_button(__('Generate QR Code'), function() {
            generateAssetQR(frm.doc.name);
        });
        
        frm.add_custom_button(__('Maintenance History'), function() {
            showMaintenanceHistory(frm.doc.name);
        });
    },
    
    rack: function(frm) {
        // Auto-populate position when rack is selected
        if (frm.doc.rack) {
            frappe.call({
                method: "dcim_theme.api.get_next_available_u",
                args: { rack: frm.doc.rack },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value("position_u", r.message);
                    }
                }
            });
        }
    }
});
