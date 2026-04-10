// DCIM PLUS - Desk Customization
// Wait for Frappe to be fully ready
frappe.ready(function() {
    console.log("DCIM PLUS Custom Theme Loaded");
    
    // Function to hide unwanted menu items
    function customizeUserMenu() {
        // Hide Help menu items
        $('.dropdown-help, .help-dropdown, a[href*="help"]').hide();
        
        // Hide View Website, Apps from user menu
        $('.dropdown-menu .dropdown-item').each(function() {
            var text = $(this).text();
            if (text.indexOf('Apps') >= 0 || 
                text.indexOf('View Website') >= 0 || 
                text.indexOf('Help') >= 0) {
                $(this).hide();
            }
        });
        
        // Also hide by href
        $('a[href*="/app/apps"], a[href*="website"], a[href*="help"]').hide();
    }
    
    // Function to add theme toggle
    function addThemeToggle() {
        if ($('.dcim-theme-toggle').length === 0) {
            $('.navbar .navbar-nav').append(`
                <li class="nav-item dcim-theme-toggle" style="margin-left: 10px;">
                    <a class="nav-link" href="#" style="cursor: pointer;">
                        <i class="fa fa-moon"></i>
                    </a>
                </li>
            `);
            
            $('.dcim-theme-toggle').click(function(e) {
                e.preventDefault();
                $('body').toggleClass('light');
                var isLight = $('body').hasClass('light');
                localStorage.setItem('dcim_theme', isLight ? 'light' : 'dark');
                $(this).find('i').toggleClass('fa-moon fa-sun');
            });
        }
    }
    
    // Apply customizations after a short delay (for dynamic content)
    setTimeout(function() {
        customizeUserMenu();
        addThemeToggle();
    }, 500);
    
    // Re-apply after page navigation (for Frappe's PJAX)
    $(document).on('page-load', function() {
        setTimeout(function() {
            customizeUserMenu();
        }, 500);
    });
});
