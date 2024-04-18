document.addEventListener('DOMContentLoaded', function() {
    render_page();
    
    document.getElementById('send_magic_link').addEventListener('click', function() {
        send_magic_link();
    });
});