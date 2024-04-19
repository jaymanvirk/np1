document.addEventListener('DOMContentLoaded', function() {

    const element_sml = document.getElementById('send_magic_link')
    if (element_sml) {
        element_sml.addEventListener('click', function() {
            send_magic_link();
        });
    }
    
});