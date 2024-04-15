async function check_session_id(){
    const response = await fetch('/user_auth/check_session_id', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    if (response.ok) {
        const data = await response.json();
        console.log(data);
    } else {
        console.error(response.statusText);
    }
}