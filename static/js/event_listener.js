document.addEventListener('DOMContentLoaded', function() {

    const element_ids = [
                        'send_sign_in_link'
                        , 'start_streaming'
                        , 'stop_streaming'
                    ]
    element_ids.forEach(id => {
        const element = document.getElementById(id)
        if (element) {
            element.addEventListener('click', () => {
                const func = window[id];
                func();
            });
        }
    })
    
});