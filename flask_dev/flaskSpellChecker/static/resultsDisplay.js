$(document).ready(function () {

    // Set cursor to hand to show that area is clickable
    var textArea = $("#textArea");
    textArea.css({ cursor: 'pointer' });

    // Get word on double click
    textArea.dblclick(function (e) {
        var selection = window.getSelection() || document.getSelection() || document.selection.createRange();
        var word = $.trim(selection.toString());
        if (word != '') {
            // // Open contextmenu on double-click (inside the text area)
            $(".context-menu").finish().toggle(100).

                // In the right position (the mouse)
                css({
                    top: e.pageY + "px",
                    left: e.pageX + "px"
                });

            // Ajax integration: selected word is forwarded to backend through POST request
            $.ajax({
                type: "POST",
                url: "http://localhost:5000/",
                cache: false,
                dataType: "json",
                data: {
                    'test': word
                },
                success: function (suggestions) {
                    //alert(data);
                    console.log(suggestions);
                    //response(suggestions);
                },
            });
        }
    });
});


// Open contextmenu on right-click (inside the text area)
$("#textArea").bind("contextmenu", function (event) {
    // Avoid the default contextMenu
    event.preventDefault();

    // Show contextmenu
    $(".context-menu").finish().toggle(100).

        // In the right position (the mouse)
        css({
            top: event.pageY + "px",
            left: event.pageX + "px"
        });
});


// If the document is clicked somewhere
$(document).bind("mousedown", function (e) {
    // If the clicked element is not the menu
    if (!$(e.target).parents(".context-menu").length > 0) {

        // Hide it
        $(".context-menu").hide(100);
    }
});


// If the menu element is clicked
$(".context-menu li").click(function () {

    // Print the name
    alert($(this).attr("data-action"))

    // Hide it AFTER the action was triggered
    $(".context-menu").hide(100);
});