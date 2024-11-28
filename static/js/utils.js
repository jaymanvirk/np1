function scroll_to_bottom() {
    window.scrollTo(0, document.body.scrollHeight);
}


function get_html_message() {
    html = `
        <div class="message">
            <div class="sender display-ib">
                <span class="name">
                </span>
                <span class="colon">
                    :
                </span>
            </div>
            <div class="media-content display-ib">
            </div>
        </div>
        `

    return html
}

function process_message(data){
    data = JSON.parse(data)
}
