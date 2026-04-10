// DCIM PLUS - Desk Customization
frappe.ready(function() {
    console.log("DCIM PLUS Custom Theme Loaded");
    
    // Hide unwanted menu items
    setTimeout(function() {
        // Hide Help menu items
        $('.dropdown-help, .help-dropdown, a[href*="help"]').hide();
        
        // Hide View Website, Apps from user menu
        $('.dropdown-item:contains("View Website"), .dropdown-item:contains("Apps"), .dropdown-item:contains("Help")').hide();
        
        // Add custom footer if needed
        if ($('.custom-footer').length === 0) {
            $('body').append(`
                <div class="custom-footer" style="display: none;">
                    © 2024 DCIM PLUS - Developed by Gemtad | Addis Ababa, Ethiopia
                </div>
            `);
        }
        
        // Add theme toggle if not exists
        if ($('.theme-toggle-btn').length === 0) {
            $('.navbar').append(`
                <button class="theme-toggle-btn" style="background: none; border: none; cursor: pointer; margin-left: 10px;">
                    <i class="fa fa-moon"></i>
                </button>
            `);
            
            $('.theme-toggle-btn').click(function() {
                $('body').toggleClass('light');
                localStorage.setItem('theme', $('body').hasClass('light') ? 'light' : 'dark');
            });
        }
    }, 1000);
});
