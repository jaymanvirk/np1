document.addEventListener('DOMContentLoaded', function() {


    const button_sign_in_link = document.getElementById('send_sign_in_link');
    if (button_sign_in_link){
        button_sign_in_link.addEventListener('click', send_sign_in_link);
    }

    const zone_drag_drop_image = document.getElementById('drop_image');
    if (zone_drag_drop_image){
        zone_drag_drop_image.addEventListener('dragover', drag_image);
        zone_drag_drop_image.addEventListener('drop', drop_image);
    }

    const button_select_image = document.getElementById('select_image');
    if (button_select_image){
        button_select_image.addEventListener('change', handle_select_image);
    }

});