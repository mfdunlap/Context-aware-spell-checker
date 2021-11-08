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
  textArea.dblclick(function (event) {
    var selection = window.getSelection();
    var word = $.trim(selection.toString());

    console.log(word);
    displayMisspellings(word, event);
  });
});

// Get word on right click
$("#textArea").bind("contextmenu", function (event) {
  // Avoid the default contextMenu
  event.preventDefault();

  var selection = window.getSelection();
  var word = selectionToString(selection);

  console.log(word);
  displayMisspellings(word, event);
});

function displayMisspellings(wordToCheck, event) {
  // Get the list of suggested corrections for the selected word if it is misspelled
  // Display mispellings in a context menu

  $.ajax({
    type: "POST",
    url: "http://localhost:5000/selected",
    cache: false,
    dataType: "json",
    data: {
      'test': wordToCheck,
    },

    // If word is misspelled
    success: function (suggestions) {
      docArea = "textArea"
      misspelling = '<span style="text-decoration: underline 2px red;">' + wordToCheck + '</span>'
      menu = ".context-menu"
      menuItem = ".context-menu li"
      menuItemID = '#listItems'
      console.log(suggestions);

      setMenuItems(menuItemID, suggestions);
      console.log(document.getElementById("contextMenu").innerHTML);

      showMenu(menu, event);

      // If a menu item is clicked
      $(menuItem).click(function () {

        replaceMisspellingWithItem(docArea, misspelling, this);
        hideMenu(menu);
      });

      // If the document is clicked somewhere else
      $(document).bind("mousedown", function (event) {
        if (!$(event.target).parents(menu).length > 0) {
          hideMenu(menu);
        }
      });
    },
  });
}

function setMenuItems(menu, items) {
  var menuItems = ''

  for (var item in items) {
    var itemVal = items[item];
    //console.log(itemVal);
    menuItems += '<li data-action="' + itemVal + '">' + itemVal + '</li>';
  }

  $(menu).empty().append(menuItems);
}

function showMenu(menu, event) {
  $(menu).finish().toggle(100).
    css({
      top: event.pageY + "px",
      left: event.pageX + "px"
    });
}

function replaceMisspellingWithItem(docArea, misspelling, item) {
  var correction = $(item).attr("data-action");
  document.getElementById(docArea).innerHTML = document.getElementById(docArea).innerHTML.replace(misspelling, correction);

}

function hideMenu(menu) {
  $(menu).hide(100);
}

function selectionToString(selection) {
  var range = selection.getRangeAt(0);
  var node = selection.anchorNode;

  while (range.toString().indexOf(' ') != 0 && range.startOffset != 0) {
    range.setStart(node, (range.startOffset - 1));
  }
  range.setStart(node, range.startOffset);

  do {
    range.setEnd(node, range.endOffset + 1);
  } while (range.toString().indexOf(' ') == -1 && range.toString().trim() != '' && range.endOffset < range.endContainer.length);

  return range.toString().trim();
}