async function send_magic_link(){
    const email =  document.getElementById('email').value;

    const response = await fetch("/user_management/send_magic_link", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"email":email})
    });

    if (response.ok) {
        const data = await response.json();
        console.log(data);
    } else {
        console.error(response.statusText);
    }
}