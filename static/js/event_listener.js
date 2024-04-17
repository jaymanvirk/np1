document.addEventListener('DOMContentLoaded', function() {
    set_user_cookie();

    document.getElementById('send_magic_link').addEventListener('click', function() {
        send_magic_link();
    });

});