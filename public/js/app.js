(function() {
    'use strict';
    
    const workspaceMap = {
        '⚡ Power Management': '/app/power-management',
        '❄️ Cooling Infrustructure': '/app/cooling-infrustructure',
        '💻 IT Asset Management': '/app/it-asset-management',
        '🛠️ Operations': '/app/operations',
        '👥 Shift & Compliance': '/app/shift-compliance',
        '📋 Vendor & Audit': '/app/vendor-audit',
        '🔒 Security & Safety': '/app/security-safety',
        'Smart DC': '/app/smart-dc',
        '📊 Infrastructure Management': '/app/infrastructure-management'
    };
    
    const iframe = document.getElementById('workspace-frame');
    const sidebar = document.getElementById('dcim-sidebar');
    const menuToggle = document.getElementById('menuToggle');
    const logoutBtn = document.getElementById('logoutBtn');
    const pageTitle = document.getElementById('pageTitle');
    
    frappe.ready(function() {
        loadUserInfo();
        setupNavigation();
    });
    
    function loadUserInfo() {
        frappe.call({
            method: "frappe.auth.get_logged_user",
            callback: function(r) {
                if (r.message) {
                    const userName = document.getElementById('userName');
                    const userAvatar = document.getElementById('userAvatar');
                    if (userName) userName.textContent = r.message;
                    if (userAvatar) userAvatar.textContent = r.message.charAt(0).toUpperCase();
                }
            }
        });
    }
    
    function setupNavigation() {
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                const workspaceName = this.getAttribute('data-workspace');
                const workspaceUrl = workspaceMap[workspaceName];
                
                if (workspaceUrl) {
                    navItems.forEach(nav => nav.classList.remove('active'));
                    this.classList.add('active');
                    pageTitle.textContent = workspaceName;
                    iframe.src = workspaceUrl;
                    
                    iframe.onload = function() {
                        hideFrappeUI();
                    };
                }
            });
        });
        
        if (menuToggle) {
            menuToggle.addEventListener('click', function() {
                sidebar.classList.toggle('mobile-open');
            });
        }
        
        if (logoutBtn) {
            logoutBtn.addEventListener('click', function() {
                frappe.call({
                    method: "frappe.auth.logout",
                    callback: function() {
                        window.location.href = '/login';
                    }
                });
            });
        }
    }
    
    function hideFrappeUI() {
        try {
            const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
            if (!iframeDoc) return;
            
            const style = iframeDoc.createElement('style');
            style.textContent = `
                .desk-sidebar, .navbar, .page-head, .toolbar,
                #navbar-breadcrumbs, .app-logo, .navbar-brand,
                .indicator-pill, .awesome-bar, .sidebar, .footer, #toolbar {
                    display: none !important;
                }
                .page-container, .layout-main-section-wrapper {
                    margin-left: 0 !important;
                    padding-top: 0 !important;
                }
                .layout-main-section {
                    width: 100% !important;
                }
            `;
            iframeDoc.head.appendChild(style);
        } catch(e) {
            console.log('Cannot inject styles', e);
        }
    }
    
    iframe.onload = function() {
        hideFrappeUI();
    };
})();
