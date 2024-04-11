document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('send_magic_link').addEventListener('click', function() {
        send_magic_link();
    });

    document.getElementById('get_user_list').addEventListener('click', function() {
        get_user_list();
    });
});