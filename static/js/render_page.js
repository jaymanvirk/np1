async function render_page(){
    const response = await fetch('/user_management/set_user_cookie', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    if (response.ok) {
        const data = await response.json();
        document.body.innerHTML = data;
        document.dispatchEvent(new Event('DOMContentLoaded'));
    } else {
        console.error(response.statusText);
    }
}

window.onload = function() {
    render_page();
}