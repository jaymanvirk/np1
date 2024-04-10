async function get_user_list(){
    const response = await fetch('/get_user_list', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    if (response.ok) {
        const data = await response.json();
        const result = JSON.parse(data.data.replace(/'/g, '"'));
        console.log(result);
    } else {
        console.error(response.statusText);
    }
}