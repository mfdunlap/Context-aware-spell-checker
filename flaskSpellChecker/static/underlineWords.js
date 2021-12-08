/*
Author: Lorenzo

To include in your html code:
<script src = "{{url_for('static', filename='underlineWords.js')}}"></script>

*/


// Underline misspelled words
$(document).ready(function () {

  document.getElementById("textArea").onkeyup = function (e) {

    text_value = $("#textArea").text();

    if (e.key == " " || e.key == "Backspace") {
      
      spaceKey = "&nbsp"
      textSingleton.cleanWords()

      // Ajax post request -> send text to backend
      $.ajax({
        type: "POST",
        url: "/",
        dataType: "json",
        cache: false,
        data: {
          'text': text_value
        },
        // Return misspelled words -> underlining misspelled words
        // data = misspelled words
        success: function (data) {
          //console.log(text_value)
          console.log("misspelled word from backend:", data)
          tmp = text_value

          textSingleton.updateText(tmp)
          console.log("current plain text: ", textSingleton.getPlainText())
          
          // If there are misspelled words
          if (data){
            textSingleton.updateMisspelledWords(data)
            
            // Remove underlines if Backspace is pressed
            if(e.key=="Backspace"){
              textSingleton.removeUnderlines()
              // Set cursor at the end of text area
              elem = document.getElementById("textArea")
              setEndOfContenteditable(elem);
              return
            }
            
            textSingleton.replaceHtmlText()
          }

          // update html text
          console.log("[DEBUG] text html:", document.getElementById("textArea").innerHTML)
          textSingleton.updateHtmlText(document.getElementById("textArea").innerHTML)
          textSingleton.printWordList()

          // Set cursor at the end of text area
          elem = document.getElementById("textArea")
          setEndOfContenteditable(elem);
        },
      });
    }
  }

});


function searchStringInArray (str, strArray) {
  for (var j=0; j<strArray.length; j++) {
      if (strArray[j].match(str)) return true;
  }
  return false;
}

// Set cursor at the end of text area || TODO: eliminate, this is wrong (cursor shouldn't slide to the end)
function setEndOfContenteditable(contentEditableElement) {
  var range, selection;
  if (document.createRange)//Firefox, Chrome, Opera, Safari, IE 9+
  {
    range = document.createRange();//Create a range (a range is a like the selection but invisible)
    range.selectNodeContents(contentEditableElement);//Select the entire contents of the element with the range
    range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
    selection = window.getSelection();//get the selection object (allows you to change selection)
    selection.removeAllRanges();//remove any selections already made
    selection.addRange(range);//make the range you have just created the visible selection
  }
  else if (document.selection)//IE 8 and lower
  {
    range = document.body.createTextRange();//Create a range (a range is a like the selection but invisible)
    range.moveToElementText(contentEditableElement);//Select the entire contents of the element with the range
    range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
    range.select();//Select the range (make it the visible selection)
  }
}

function arraysMatch(arr1, arr2) {

  // Check if the arrays are the same length
  if (arr1.length !== arr2.length) return false;

  // Check if all items exist and are in the same order
  for (var i = 0; i < arr1.length; i++) {
    if (arr1[i] !== arr2[i]) return false;
  }

  // Otherwise, return true
  return true;
};

function checkBackspace(key, data) {

  //if ((key == "Backspace") && (!(arraysMatch(textSingleton.getMisspelledWords(), data)))) {
  if(key=="Backspace"){
    textSingleton.removeUnderlines()
    // Set cursor at the end of text area
    elem = document.getElementById("textArea")
    setEndOfContenteditable(elem);
    return true;
  }

  else return false;
}

function cleanHtmlTextFromUnderlines(htmlText) {
  htmlText = htmlText.replace('<span style="text-decoration: underline 2px red;">', '')
  htmlText = htmlText.replace('</span>', '')
  document.getElementById("textArea").innerHTML = htmlText
  textSingleton.updateHtmlText(htmlText)
  textSingleton.updateText(htmlText)
}