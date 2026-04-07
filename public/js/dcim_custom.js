// DCIM Plus - Main Application
frappe.ready(function() {
    console.log('DCIM Plus loading...');
    
    // Check if we're on the dcim page
    if (window.location.pathname === '/dcim') {
        initDCIM();
    }
});

function initDCIM() {
    // Create app container if not exists
    if (!document.getElementById('dcim-app')) {
        createApp();
    }
    
    // Load dashboard
    loadDashboard();
}

function createApp() {
    // Clear body
    document.body.innerHTML = '';
    document.body.style.margin = '0';
    document.body.style.padding = '0';
    
    // Create app structure
    const app = document.createElement('div');
    app.id = 'dcim-app';
    app.innerHTML = `
        <div class="dcim-header">
            <h1>🏢 DCIM PLUS</h1>
        </div>
        <div id="dcim-content"></div>
    `;
    document.body.appendChild(app);
}

function loadDashboard() {
    const content = document.getElementById('dcim-content');
    if (!content) return;
    
    content.innerHTML = `
        <div class="stats-grid">
            <div class="stat-box">
                <div class="stat-number" id="rackCount">--</div>
                <div class="stat-label">Total Racks</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" id="deviceCount">--</div>
                <div class="stat-label">Active Devices</div>
            </div>
        </div>
        <div class="dcim-card">
            <h3>📊 System Status</h3>
            <p style="color:#94a3b8;">DCIM Plus is operational. Loading data from Frappe...</p>
        </div>
    `;
    
    // Fetch real data
    frappe.call({
        method: "frappe.client.get_count",
        args: { doctype: "Rack" },
        callback: function(r) {
            const el = document.getElementById('rackCount');
            if (el) el.textContent = r.message || 0;
        }
    });
    
    frappe.call({
        method: "frappe.client.get_count",
        args: { doctype: "IT Asset", filters: { status: "Active" } },
        callback: function(r) {
            const el = document.getElementById('deviceCount');
            if (el) el.textContent = r.message || 0;
        }
    });
}
