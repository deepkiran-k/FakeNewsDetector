const server_env = window.location.pathname.includes("/claimbuster-dev") ? "/claimbuster-dev" : "/claimbuster";
const idir_email = "vqveyno@hgn.rqh".replace(/[a-zA-Z]/g, function(c) {return String.fromCharCode((c <= "Z" ? 90 : 122) >= (c = c.charCodeAt(0) + 13) ? c : c - 26);});

function simulateLink(event, element, _url=null) {
    let mouse_button = event.which;
    let url = _url !== null ? _url : $(element).attr("url");

    if (mouse_button === 1 && !event.ctrlKey) {
        window.location.href = url;
    }
    else if (mouse_button === 2 || (mouse_button === 1 && event.ctrlKey)) {
        window.open(url, '_blank');
    }
}

$(document).ready(function () {
    $('.main.menu').visibility({
        type: 'fixed'
    });

    $('.image').visibility({
        type: 'image',
        transition: 'vertical flip in',
        duration: 500
    });

    $('.email-idir').click(function (e) {
        window.open(`mailto:${idir_email}`);
    });

    $('.home-link').mousedown(function(e) {
        simulateLink(e, this, `${server_env}/`);
    });
});