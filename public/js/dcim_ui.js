/* ============================================
   DCIM PLUS - UI ENHANCEMENTS
   Non-intrusive, Frappe-friendly
   ============================================ */

frappe.ready(function() {
    console.log("🎨 DCIM PLUS UI Enhancements Loaded");
    
    // Add custom footer branding (doesn't remove existing)
    addCustomFooter();
    
    // Enhance sidebar with smooth animations
    enhanceSidebar();
    
    // Add live datetime to navbar (optional)
    addLiveDateTime();
});

function addCustomFooter() {
    // Only add if not already present
    if (document.querySelector('.dcim-footer-brand')) return;
    
    const footer = document.querySelector('footer');
    if (footer) {
        const brandSpan = document.createElement('div');
        brandSpan.className = 'dcim-footer-brand';
        brandSpan.style.cssText = 'font-size: 10px; color: #6B7280; margin-top: 8px; text-align: center;';
        brandSpan.innerHTML = '🏭 DCIM PLUS | Powered by Frappe | © Awash Bank';
        footer.appendChild(brandSpan);
    }
}

function enhanceSidebar() {
    const items = document.querySelectorAll('.sidebar-item');
    items.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.2s ease';
        });
    });
}

function addLiveDateTime() {
    if (document.querySelector('.dcim-datetime')) return;
    
    const navbar = document.querySelector('.navbar-collapse');
    if (navbar) {
        const dateSpan = document.createElement('div');
        dateSpan.className = 'dcim-datetime';
        dateSpan.style.cssText = 'font-size: 11px; color: #6B7280; margin-left: auto; padding: 0 15px;';
        
        function updateTime() {
            const now = new Date();
            dateSpan.innerHTML = now.toLocaleTimeString('en-US', { hour12: false });
        }
        updateTime();
        setInterval(updateTime, 1000);
        
        navbar.appendChild(dateSpan);
    }
}
