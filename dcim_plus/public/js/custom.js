
frappe.ready(function() {
    // Redirect logo click to home page
    $('.navbar-brand').on('click', function(e) {
        e.preventDefault();
        window.location.href = '/home-2';
    });
    
    // Also handle if there are multiple logo elements
    $('.navbar-brand img, .navbar-brand .brand-logo').on('click', function(e) {
        e.preventDefault();
        window.location.href = '/home-2';
    });
});
