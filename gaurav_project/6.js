/*
 * Script to facilitate passing annotated text to Claim Checker System
 * Written by: Josue Caraballo
 */
function claimCheckerInterface() {
    /* Function which will:
     *  1) Remove any existing selected text popups
     *  2) create a new popup on the sentence the user clicked
     *  3) add some classes for presentation
     */
    removePopups();
    let anchorTag = $(this);

    if (!anchorTag.popup("exists")) {
        anchorTag.popup({
            html: "<a class='noStyle' style='color: black; font-weight: bold;' href='javascript:claimCheckerPipeline();'>Fact-check this</a>",
            on: 'manual',
            hoverable: true,
            onHide: function () {
                anchorTag.removeClass('selectedText');
            }
        });
    }

    anchorTag.popup("show");
    anchorTag.addClass('selectedText');
}

function claimCheckerPipeline() {
    /*
     * Function which will:
     *   1) Get text contained in item which has been clicked
     *   2) Draw presentation layer and then populate it with a "loading" widget
     *   3) Send text as input to api in Claim Checker
     *   4) When results arrive, replace step (2) with results as demonstrated in VLDB paper
     */
    /*declarations*/
    const loadingHTML = '<div class="ui active centered inline large text loader">Fetching Results</div>';
    const errorHTML = '<div class="ui red icon message"><i class="times icon"></i><div class="content"><div class="header">Oops! Something Went Wrong.</div><p>Please try again later, or try another sentence.</p></div></div>';
    let presentationLayer = $('#factCheckerPresentation');
    let knowledgeBaseLayer = $('#knowledgeBases');
    let factMatcherLayer = $('#factMatcher');
    let semanticSearchLayer = $('#semanticSearch');
    let input = $('.selectedText').text();
    let input_encoded = encodeURIComponent(input);

    removePopups();

    let populateFactCheckerPresentation = function (element) {
        return function (response, textStatus, jqXHR) {
            element.html(response)
        }
    };

    let populateFactCheckerPresentationError = function (element) {
        return function (jqXHR, textStatus, errorThrown) {
            if (element) {
                element.html(errorHTML);
            } else {
                console.log("[ERROR] You forgot to set the module destination in the error handling function for the AJAX request!");
            }
        }
    };

    $.each([knowledgeBaseLayer, factMatcherLayer, semanticSearchLayer], function (index, element) {element.html(loadingHTML);});
    // $.each([knowledgeBaseLayer, factMatcherLayer], function (index, element) {element.html(loadingHTML);});
    if (presentationLayer.hasClass('hidden')) {
        presentationLayer.transition("slide down");
    }

    $.ajax({
        url: `${server_env}/factchecker/get/html/ss/` + input_encoded,
        success: populateFactCheckerPresentation(semanticSearchLayer),
        error: populateFactCheckerPresentationError(semanticSearchLayer)
    });

    $.ajax({
        url: `${server_env}/factchecker/get/html/kb/` + input_encoded,
        success: populateFactCheckerPresentation(knowledgeBaseLayer),
        error: populateFactCheckerPresentationError(knowledgeBaseLayer)
    });
    
    $.ajax({
        url: `${server_env}/factchecker/get/html/fm/` + input_encoded,
        success: populateFactCheckerPresentation(factMatcherLayer),
        error: populateFactCheckerPresentationError(factMatcherLayer)
    });
}

function removePopups() {
    $(document).popup("hide all");
}

$(document).on("click", ".divTranscript > span, .divTranscript > div > span", claimCheckerInterface);