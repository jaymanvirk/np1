function scroll_to_bottom() {
    window.scrollTo(0, document.body.scrollHeight);
}


function get_message(data) {
    //TODO:
    //check for the flag "thought complete" to add new message or update existing one
    data = JSON.parse(data)
    html = `
        <div class="message">
            <div class="sender display-ib">
                <span class="name">
                    ${data.sender.name}
                </span>
                <span class="colon">
                    :
                </span>
            </div>
            <div class="media-content display-ib">
                ${data.media.text}
            </div>
        </div>
        `

    return html
}
