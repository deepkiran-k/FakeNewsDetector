const server_env = window.location.pathname.includes("/claimbuster-dev") ? "/claimbuster-dev" : "/claimbuster";
const idir_email = "vqveyno@hgn.rqh".replace(/[a-zA-Z]/g, function(c) {return String.fromCharCode((c <= "Z" ? 90 : 122) >= (c = c.charCodeAt(0) + 13) ? c : c - 26);});
let api_calls = [];
let fyot_kb = $('#fyot .kb');
let fyot_fm = $('#fyot .fact-match');
let syot = $('.score-your-own-text');

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

function getUserInput() {
  return $(".ui.segment.visible input, .ui.segment.visible textarea").val();
}

function htmlEscape(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function updateResults(component="") {
    let filter_list = ["’", "‘", "‛", "❛", "❜", "‹", "›", "«", "»", "“", "”", "„", "‟", "❝", "❞"];
    let user_input = getUserInput();

    if (user_input === "") {
        return;
    }

    $.each(filter_list, function (index, value) {
        user_input = user_input.replace(value, "\"");
    });

    api_calls.forEach(function (call) {
        call.abort();
    });

    api_calls = [];

    if(component === "fyot"){
        fyot_kb.empty().html('<div class="ui active centered inline large text loader">Fetching Results</div>');
        fyot_fm.empty().html('<div class="ui active centered inline large text loader">Fetching Results</div>');

        api_calls.push($.get(`./get/html/kb/${user_input}`).done(function (kb_html) {
            console.log(kb_html);
            fyot_kb.html(kb_html);
        }));

        api_calls.push($.get(`./get/html/fm/${user_input}`).done(function (fm_html) {
            fyot_fm.html(fm_html);
        }));
    } else if (component === "syot") {
        syot.empty().html("<div class=\"ui active centered inline large text loader\">Scoring Your Sentence(s)</div>");

        api_calls.push(
          $.ajax({
            type: "POST",
            url: './get/html/syot/',
            data: JSON.stringify({claim: user_input}),
            beforeSend: function(xhrObj){
              xhrObj.setRequestHeader("Content-Type", "application/json");
            },
            success: function(syot_html){ syot.html(syot_html); }
          })
        );
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

    $(".ui.fluid.buttons button").click(function() {
        let _this = $(this);
        let visible_element = $(".ui.basic.segment.visible");
        let hidden_element = $(".ui.basic.segment.hidden");

        if (!_this.hasClass("blue") && !visible_element.transition("is animating") && !hidden_element.transition("is animating")) {
            _this.addClass("blue");
            _this.siblings("button").removeClass("blue");
            visible_element.transition({
                animation: 'horizontal flip',
                onComplete: function() {
                    hidden_element.transition("horizontal flip");
            }});
        }
    });

    $(".input .ui.icon.button, .input .ui.corner.label").click(function() {
        updateResults($(this).attr("component"));
    });

    $("#fyot input").keypress(function(e) {
        if (e.keyCode === 13 || (e.keyCode === 10 && e.ctrlKey)) {
            updateResults("fyot");
        }
    });

    $("#syot textarea").keypress(function(e) {
        if (e.keyCode === 13 && !e.ctrlKey) {
            updateResults("syot");
        }
        else if (e.keyCode === 10 && e.ctrlKey) {
            $(this).val(function (i, val) {
                return `${val}\n`;
            });
        }
    });
});