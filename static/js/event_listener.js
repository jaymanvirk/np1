document.addEventListener('DOMContentLoaded', function() {
    const button_sign_in_link = document.getElementById('send_sign_in_link');
    if (button_sign_in_link){
        button_sign_in_link.addEventListener('click', send_sign_in_link);
    }

    const button_stream_audio = document.getElementById('chat_log');
    if (button_stream_audio){
        stream_audio();
    }

});