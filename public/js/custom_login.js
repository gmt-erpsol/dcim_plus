frappe.ready(function() {
    // Hide email login option
    setTimeout(function() {
        $('.login-option').hide();
        $('.btn-login-with-email-link').hide();
        $('#login-email').hide();
        
        // Remove any email login related text
        $('.forgot-password-message').text('Forgot Password?');
        
        // Change welcome message
        $('.login-title').text('Welcome to Awash Bank DCIM Plus');
        $('.login-subtitle').text('Secure Data Center Management');
        
        // Remove footer logo text
        $('.footer-logo').text('');
        $('.footer-logo').append('<img src="/assets/dcim_plus/images/awash-footer-logo.png" height="30">');
        
        // Add bank info to footer
        if ($('.footer-copyright').length) {
            $('.footer-copyright').html('© 2024 Awash Bank | Addis Ababa, Ethiopia');
        }
    }, 100);
});
