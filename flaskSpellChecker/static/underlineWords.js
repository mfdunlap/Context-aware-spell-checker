/*
Author: Lorenzo

To include in your html code:
<script src = "{{url_for('static', filename='underlineWords.js')}}"></script>

*/

// class for text management
class textClass {

  #text;
  #htmlText;
  #misspelledWords;

  constructor(text = '', htmlText = '', misspelledWords = []) {
    this.#text = text
    this.#htmlText = htmlText
    this.#misspelledWords = misspelledWords
  }

  getPlainText() {
    return this.#text;
  }
  updateText(tmp) {
    this.#text = tmp;
  }
  getHtmlText() {
    return this.#htmlText;
  }
  updateHtmlText(newHtmlText) {
    this.#htmlText = newHtmlText;
  }
  getMisspelledWords() {
    return this.#misspelledWords;
  }
  updateMisspelledWords(misspelledWordsList) {
    this.#misspelledWords = misspelledWordsList;
  }

};

// global text instance
var textSingleton = new textClass()

// Underline misspelled words
$(document).ready(function () {

  document.getElementById("textArea").onkeyup = function (e) {
    //var text_value = document.getElementById("textArea");

    text_value = $("#textArea").text();

    text_html = document.getElementById("textArea");
    text_html = text_html.innerHTML

    //console.log(text_value.at(-1))

    if (e.key == " " || (e.key == "Backspace")) {
      //console.log("DETECTED")

      // Ajax post request -> send text to backend
      $.ajax({
        type: "POST",
        url: "http://localhost:5000/",
        dataType: "json",
        cache: false,
        data: {
          'text': text_value
        },
        // Return mispelled words -> underlining misspelled words
        success: function (data) {
          //console.log(text_value)
          //console.log(data)
          tmp = text_value

          // check if misspelled word has been manually corrected using backspace
          if (checkBackspace(e.key, data, tmp))
            return

          // update plain text (no html)
          textSingleton.updateText(tmp)
          console.log("current plain text: ", textSingleton.getPlainText())

          // update misspelled words in the text
          textSingleton.updateMisspelledWords(data)
          console.log("current misspelled words: ", textSingleton.getMisspelledWords())

          for (let i = 0; i < data.length; i++) {
            word = data.at(i)
            tmp = tmp.replace(word, '<span style="text-decoration: underline 2px red;">' + word + '</span>');
            document.getElementById("textArea").innerHTML = tmp
            console.log(tmp)
          }


          // update html text
          textSingleton.updateHtmlText(document.getElementById("textArea").innerHTML)
          console.log("current html text: ", textSingleton.getHtmlText())

          //$("textArea").css('text-decoration','underline')

          // Set cursor at the end of text area
          elem = document.getElementById("textArea")
          setEndOfContenteditable(elem);

          //$("#textArea").value = underlinedText.css('text-decoration', 'underline')

          //alert(data);
          //console.log(data);
          //response(data);
        },
        //error: function(jqXHR, textStatus, errorThrown) {
        //    console.log(textStatus + " " + errorThrown);
        //}
      });
    }
  }

});

// Set cursor at the end of text area
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
    range.select();//Select the range (make it the visible selection
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

function checkBackspace(key, data, text) {

  if ((key == "Backspace") && (!(arraysMatch(textSingleton.getMisspelledWords(), data)))) {
    cleanHtmlTextFromUnderlines(text)
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
