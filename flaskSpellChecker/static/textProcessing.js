/*
Author: Lorenzo and Maya

To include in your html code:
<script src = "{{url_for('static', filename='textProcessing.js')}}"></script>
*/

// Get word by cursor selection
$(document).ready(function () {
  // Set cursor to hand to show that area is clickable
  var textArea = $("#textArea");
  textArea.css({ cursor: 'pointer'});
  var textAreaElement = document.getElementById("textArea")
  // Get word on double click
  textArea.dblclick(function (event) {
    var selection = document.getSelection();
    var word = $.trim(selection.toString());

    selectedWordIndex = getSelectedWordIndex(textAreaElement, word)
    //console.log("index: ",selectedWordIndex)

    console.log("selected:",word);
    displayMisspellings(word, event, selectedWordIndex);
  });
});

// Get word on right click
$("#textArea").bind("contextmenu", function (event) {
  // Avoid the default contextMenu
  event.preventDefault();
  var textAreaElement = document.getElementById("textArea")
  var selection = window.getSelection();
  var word = selectionToString(selection);
  selectedWordIndex = getSelectedWordIndex(textAreaElement, word)
  console.log(word);
  displayMisspellings(word, event, selectedWordIndex);
});

function getSelectedWordIndex(textAreaElement, word, divId = "#textArea"){
  // This function get the index of the selected word within the text area. It support duplicate misspelled word

  // Get the offset of the last selected words' character 
  selectionOffset = getCaretCharacterOffsetWithin(textAreaElement)
  wordLength = word.length
  // Get the portion of the text from the start to the selected word
  substring = $(divId).text().substring(0, selectionOffset)
  subStringWords = substring.split(/\s/)
  let indices = []
  // Get the indices of all the potential duplicates of the words
  subStringWords.forEach((el,index) => {
    if (el==word)
      indices.push(index)
  })
  // If any, get the context of the word with the larger index (the actual selected)
  var selectedWordIndex;
  if (indices.length>1)
    selectedWordIndex = indices[indices.length-1];
  else
    selectedWordIndex = indices[0]

  return selectedWordIndex
}

function getCaretCharacterOffsetWithin(element) {
  // This utility get the offset of the last character of the selected word (the caret offset)

  var caretOffset = 0;
  var doc = element.ownerDocument || element.document;
  var win = doc.defaultView || doc.parentWindow;
  var sel;
  if (typeof win.getSelection != "undefined") {
      sel = win.getSelection();
      if (sel.rangeCount > 0) {
          var range = win.getSelection().getRangeAt(0);
          var preCaretRange = range.cloneRange();
          preCaretRange.selectNodeContents(element);
          preCaretRange.setEnd(range.endContainer, range.endOffset);
          caretOffset = preCaretRange.toString().length;
      }
  } else if ( (sel = doc.selection) && sel.type != "Control") {
      var textRange = sel.createRange();
      var preCaretTextRange = doc.body.createTextRange();
      preCaretTextRange.moveToElementText(element);
      preCaretTextRange.setEndPoint("EndToEnd", textRange);
      caretOffset = preCaretTextRange.text.length;
  }
  return caretOffset;
}


function displayMisspellings(wordToCheck, event, selectedWordIndex) {
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
      console.log("suggestions:",suggestions);

      setMenuItems(menuItemID, suggestions);
      //console.log("corrections: ", document.getElementById("contextMenu").innerHTML);

      showMenu(menu, event);

      // If a menu item is clicked
      $(menuItem).click(function () {
        //replaceMisspellingWithItem(docArea, misspelling, this);

        // Replace the misspelled word with the clicked correction.
        replaceMisspellingWithItem(selectedWordIndex, this);
        
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

function replaceMisspellingWithItem(misspellingIndex, item) {
  var correction = $(item).attr("data-action");
  //document.getElementById(docArea).innerHTML = document.getElementById(docArea).innerHTML.replace(misspelling,  correction);
  
  // Change the word within the global text istance and its html code
  textSingleton.replaceMisspelledWithCorrection(correction, misspellingIndex)
  // Replace the old html text with the new one (with the correction)
  if($("#textArea").text().length != textSingleton.getPlainText().length)
    textSingleton.updateText($("#textArea").text())
  
  textSingleton.replaceHtmlText()
  textSingleton.printWordList()
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