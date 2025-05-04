$(document).ready(function () {
    let div_ranked = $('#divRanked');
    let div_chron = $('#divChron');
    let cws_slider = $('#cws-slider');
    let chronological_select_button = $('#optionChronological');
    let ranked_select_button = $('#optionScore');
    let order_selection = "chronological";
    let default_value = 0.7;

    function updateChronologicalDiv(value, element) {
        element.children("span").each(function () {
            let color_class_val = parseFloat($(this).attr("data-colorclass"));

            $(this).removeClass();

            if (color_class_val >= value) {
                $(this).addClass("color_class_" + Math.ceil(color_class_val * 10));
            }
        });
    }

    function updateRankedDiv(value, element) {
        element.children("div").each(function() {
            if (parseFloat($(this).attr("data-score")) >= value) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }

    cws_slider.slider({
        min: 0,
        max: 1,
        start: default_value,
        step: 0.05,
        smooth: true,
        showLabelTicks: true,
        onChange: function(value) {
            if (order_selection === "chronological") {
                updateChronologicalDiv(value, $('#divChron'));
            }
            else {
                updateRankedDiv(value, $('#divRanked'));
            }
        }
    });

    cws_slider.slider("set value", default_value);

    ranked_select_button.click(function () {
        order_selection = "ranked";

        updateRankedDiv(cws_slider.slider("get value"), $('#divRanked'));
        chronological_select_button.removeClass("blue");
        ranked_select_button.addClass("blue");

        div_chron.css('display', 'none');
        div_chron.parent().css('display', 'none');
        div_chron.parent().css('width', '100%');
        div_ranked.css('display', 'block');
        div_ranked.parent().css('display', 'block');
        div_ranked.parent().css('width', '100%');
    });

    chronological_select_button.click(function () {
        order_selection = "chronological";

        updateChronologicalDiv(cws_slider.slider("get value"), $('#divChron'));
        ranked_select_button.removeClass("blue");
        chronological_select_button.addClass("blue");

        div_ranked.css('display', 'none');
        div_ranked.parent().css('display', 'none');
        div_ranked.parent().css('width', '100%');
        div_chron.css('display', 'block');
        div_chron.parent().css('display', 'block');
        div_chron.parent().css('width', '100%');
    });

    div_chron.wrap('<div/>')
        .css({'overflow': 'hidden'})
        .parent()
        .css({
            'display': 'inline-block',
            'overflow': 'hidden',
            'height': function () {
                return $('#divChron', this).height();
            },
            'width': '100%',
            'resize': 'both'
        }).find('#divChron')
        .css({
            overflow: 'auto',
            width: '100%',
            height: '100%'
        });

    div_ranked.wrap('<div/>')
        .css({'overflow': 'hidden'})
        .parent()
        .css({
            'display': 'none',
            'overflow': 'hidden',
            'height': function () {
                return $('#divRanked', this).height();
            },
            'width': '100%',
            'resize': 'both'
        }).find('#divRanked')
        .css({
            overflow: 'auto',
            width: '100%',
            height: '100%'
        });
});