from __future__ import unicode_literals
import frappe
from frappe.website.utils import get_html_template

def get_context(context):
    # This prevents Frappe from wrapping the page
    context.no_cache = 1
    context.no_sitemap = 1
    
    # Your pure HTML (the complete page you want)
    context.html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DCIM PLUS - Data Center Infrastructure Management</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0e27;
            overflow: hidden;
        }
        
        .app {
            display: flex;
            height: 100vh;
        }
        
        .sidebar {
            width: 280px;
            background: linear-gradient(180deg, #0f1535 0%, #0a0e27 100%);
            border-right: 1px solid #1a2350;
            overflow-y: auto;
        }
        
        .logo {
            padding: 28px 24px;
            border-bottom: 1px solid #1a2350;
            margin-bottom: 20px;
        }
        
        .logo h1 {
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(135deg, #2ecc71, #27ae60);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .logo p {
            color: #5a6e8a;
            font-size: 12px;
            margin-top: 8px;
        }
        
        .nav-section {
            padding: 0 16px;
            margin-bottom: 24px;
        }
        
        .nav-section-title {
            color: #5a6e8a;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 0 12px;
            margin-bottom: 12px;
        }
        
        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 16px;
            margin: 4px 0;
            border-radius: 8px;
            color: #8892b0;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .nav-item:hover {
            background: rgba(46, 204, 113, 0.08);
            color: #2ecc71;
        }
        
        .nav-item.active {
            background: rgba(46, 204, 113, 0.12);
            color: #2ecc71;
        }
        
        .nav-item i {
            width: 20px;
            font-size: 16px;
        }
        
        .main {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .topbar {
            background: rgba(15, 21, 53, 0.95);
            backdrop-filter: blur(10px);
            padding: 16px 32px;
            border-bottom: 1px solid #1a2350;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .page-title {
            color: white;
            font-size: 20px;
            font-weight: 600;
        }
        
        .user-info {
            display: flex;
            align-items: center;
            gap: 24px;
            color: #8892b0;
        }
        
        .content {
            flex: 1;
            overflow-y: auto;
            padding: 24px 32px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 20px;
            margin-bottom: 32px;
        }
        
        .stat-card {
            background: #0f1535;
            border-radius: 12px;
            padding: 20px;
            border-left: 3px solid;
        }
        
        .stat-card.critical { border-left-color: #e74c3c; }
        .stat-card.warning { border-left-color: #f39c12; }
        .stat-card.success { border-left-color: #2ecc71; }
        .stat-card.info { border-left-color: #3498db; }
        
        .stat-label {
            color: #8892b0;
            font-size: 12px;
            margin-bottom: 8px;
        }
        
        .stat-value {
            color: white;
            font-size: 32px;
            font-weight: 700;
        }
        
        .assets-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 32px;
        }
        
        .asset-card {
            background: #0f1535;
            border-radius: 10px;
            padding: 16px;
        }
        
        .asset-title {
            color: #2ecc71;
            font-size: 13px;
            margin-bottom: 8px;
        }
        
        .asset-count {
            color: white;
            font-size: 20px;
            font-weight: 600;
        }
        
        .loading {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #2ecc71;
            font-size: 24px;
        }
    </style>
</head>
<body>
    <div id="app">
        <div class="loading">
            <i class="fas fa-spinner fa-pulse"></i> Loading DCIM PLUS...
        </div>
    </div>
    
    <script src="/assets/js/frappe-web.min.js"></script>
    <script>
        let currentUser = null;
        
        async function fetchCount(doctype) {
            try {
                const res = await frappe.call('frappe.client.get_count', { doctype });
                return res.message || 0;
            } catch(e) { return 0; }
        }
        
        async function renderDashboard() {
            const [assets, racks, ups, gens] = await Promise.all([
                fetchCount('IT Asset'),
                fetchCount('Rack'),
                fetchCount('UPS'),
                fetchCount('Generator')
            ]);
            
            const html = `
                <div>
                    <h2 style="color: white; margin-bottom: 24px;">DCIM PLUS | Executive Dashboard</h2>
                    
                    <div class="stats-grid">
                        <div class="stat-card critical">
                            <div class="stat-label">CRITICAL ALERTS</div>
                            <div class="stat-value">0</div>
                        </div>
                        <div class="stat-card warning">
                            <div class="stat-label">OPEN INCIDENTS</div>
                            <div class="stat-value">0</div>
                        </div>
                        <div class="stat-card success">
                            <div class="stat-label">ACTIVE RACKS</div>
                            <div class="stat-value">${racks}</div>
                        </div>
                        <div class="stat-card info">
                            <div class="stat-label">POWER (KW)</div>
                            <div class="stat-value">0</div>
                        </div>
                    </div>
                    
                    <div class="assets-grid">
                        <div class="asset-card">
                            <div class="asset-title">🏢 Infrastructure</div>
                            <div class="asset-count">0 DC - ${racks} Racks</div>
                        </div>
                        <div class="asset-card">
                            <div class="asset-title">💻 IT Assets</div>
                            <div class="asset-count">${assets} Assets - 0 Ports</div>
                        </div>
                        <div class="asset-card">
                            <div class="asset-title">⚡ Power Mgmt</div>
                            <div class="asset-count">${ups} UPS - ${gens} Gen</div>
                        </div>
                    </div>
                </div>
            `;
            
            document.getElementById('content').innerHTML = html;
        }
        
        function navigateTo(view) {
            if (view === 'dashboard') renderDashboard();
        }
        
        async function init() {
            const sidebarHtml = `
                <div class="sidebar">
                    <div class="logo">
                        <h1><i class="fas fa-database"></i> DCIM PLUS</h1>
                        <p>Addis Ababa, Ethiopia</p>
                    </div>
                    <div class="nav-section">
                        <div class="nav-section-title">MAIN</div>
                        <div class="nav-item active" data-view="dashboard">
                            <i class="fas fa-tachometer-alt"></i>
                            <span>Dashboard</span>
                        </div>
                    </div>
                    <div class="nav-section">
                        <div class="nav-section-title">INFRASTRUCTURE</div>
                        <div class="nav-item" data-view="racks">
                            <i class="fas fa-server"></i>
                            <span>Racks</span>
                        </div>
                    </div>
                    <div class="nav-section">
                        <div class="nav-section-title">ASSETS</div>
                        <div class="nav-item" data-view="it-assets">
                            <i class="fas fa-microchip"></i>
                            <span>IT Assets</span>
                        </div>
                    </div>
                </div>
                <div class="main">
                    <div class="topbar">
                        <div class="page-title">Executive Dashboard</div>
                        <div class="user-info">
                            <i class="fas fa-bell"></i>
                            <span id="user-name">${frappe.session.user || 'Admin'}</span>
                            <i class="fas fa-user-circle"></i>
                        </div>
                    </div>
                    <div class="content" id="content"></div>
                </div>
            `;
            
            document.getElementById('app').innerHTML = sidebarHtml;
            
            document.querySelectorAll('.nav-item').forEach(item => {
                item.addEventListener('click', () => navigateTo(item.dataset.view));
            });
            
            await renderDashboard();
        }
        
        frappe.ready(() => init());
    </script>
</body>
</html>
    '''
    
    # Return the HTML directly without Frappe wrapper
    return context

# This is critical - prevents Frappe from wrapping
@frappe.whitelist(allow_guest=True)
def render_html():
    return get_context({}).html_content
