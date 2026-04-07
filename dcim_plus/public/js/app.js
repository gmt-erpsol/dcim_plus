// DCIM Plus - Simple Working Customization
(function() {
    console.log("DCIM Plus Loading...");

    // Hide Frappe navbar and footer when page loads
    function hideFrappeUI() {
        // Hide navbar
        $('.navbar').hide();
        $('.navbar-header').hide();
        $('.page-head').hide();
        
        // Hide sidebar
        $('.layout-sidebar').hide();
        $('.sidebar').hide();
        $('.col-sidebar').hide();
        
        // Hide footer
        $('.footer').hide();
        $('.page-footer').hide();
        
        // Make content full width
        $('.layout-main-section-wrapper').css('margin-left', '0');
        $('.layout-main-section').css('margin-left', '0');
        
        // Add custom class to body
        $('body').addClass('dcim-custom');
    }

    // Add custom CSS dynamically
    function addCustomStyles() {
        $('head').append(`
            <style>
                body.dcim-custom {
                    background: #0a0e27 !important;
                }
                .dcim-custom .page-content {
                    background: #0a0e27 !important;
                }
                .dcim-custom .frappe-card {
                    background: #0f1535 !important;
                    border: 1px solid #1a2350 !important;
                }
                .dcim-custom .list-row {
                    background: #0f1535 !important;
                    color: #e0e0e0 !important;
                }
            </style>
        `);
    }

    // Initialize when Frappe is ready
    frappe.ready(function() {
        console.log("Frappe Ready - Applying DCIM Customizations");
        hideFrappeUI();
        addCustomStyles();
        
        // Re-apply after page navigation
        $(document).on('page-load', function() {
            setTimeout(hideFrappeUI, 100);
        });
    });

})();
