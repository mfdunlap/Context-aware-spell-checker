/*
Author: Lorenzo and Maya

To include in your html code:
<script src = "{{url_for('static', filename='textProcessing.js')}}"></script>
*/

// Get word by cursor selection
$(document).ready(function () {
  // Set cursor to hand to show that area is clickable
  var textArea = $("#textArea");
  textArea.css({ cursor: 'pointer' });

  // Get word on double click
  textArea.dblclick(function (e) {
    var selection = window.getSelection() || document.getSelection() || document.selection.createRange();
    var word = $.trim(selection.toString())// Ajax integration: selected word is forwarded to backend through POST request

    // Get the list of suggested corrections for the selected word if it is misspelled
    console.log(word)
    $.ajax({
      type: "POST",
      url: "http://localhost:5000/selected",
      cache: false,
      dataType: "json",
      data: {
        'test': word,
      },

      // If word is misspelled
      success: function (suggestions) {
        console.log(suggestions);

        if (word != '') {
          var list_item_str = ''

          // Add each suggestion to the dropdown list
          for (var key in suggestions) {
            var suggest = suggestions[key]
            console.log(suggest)

            list_item_str += '<li data-action="' + suggest + '">' + suggest + '</li>'
          }

          // Put the new list items into the html code for the dropdown menu
          $('#listItems').empty().append(list_item_str);
          console.log(document.getElementById("contextMenu").innerHTML);

          // Show the dropdown menu
          $(".context-menu").finish().toggle(100).

            // Move it to where the mouse is clicked
            css({
              top: e.pageY + "px",
              left: e.pageX + "px"
            });

          // If the document is clicked somewhere
          $(document).bind("mousedown", function (e) {
            // If the clicked element is not the menu
            if (!$(e.target).parents(".context-menu").length > 0) {

              // Hide the menu
              $(".context-menu").hide(100);
            }
          });


          // If a menu element is clicked
          $(".context-menu li").click(function () {

            // Replaced the misspelling with the selected correction
            var correction = $(this).attr("data-action");
            document.getElementById("textArea").innerHTML = document.getElementById("textArea").innerHTML.replace(word, correction);


            // Hide the menu after the action was triggered
            $(".context-menu").hide(100);
          });
        }
      },
    });
  });
});