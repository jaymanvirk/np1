async function get_user_list(){
    const response = await fetch('/user_management/get_user_list', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    if (response.ok) {
        const data = await response.json();
        const result = JSON.parse(data.replace(/'/g, '"'));
        console.log(result);
    } else {
        console.error(response.statusText);
    }
}