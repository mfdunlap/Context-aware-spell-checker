/*
Author: Lorenzo

To include in your html code:
<script src = "{{url_for('static', filename='underlineWords.js')}}"></script>

*/

// Underline misspelled words
$(document).ready(function(){
    
    document.getElementById("textArea").onkeyup = function(e){
      //var text_value = document.getElementById("textArea");

      text_value = $("#textArea").text();
  
      text_html= document.getElementById("textArea");
      text_html = text_html.innerHTML
  
      //console.log(text_value.at(-1))

      if(e.key == " " || (e.key == "Backspace" )) {
        //console.log("DETECTED")
        
        // Ajax post request -> send text to backend
          $.ajax({
            type: "POST",
            url : "http://localhost:5000/",
            dataType : "json",
            cache: false,
            data : {
                'text' : text_value
            },
            // Return mispelled words -> underlining misspelled words
            success : function(data) {
<<<<<<< HEAD:flask_dev/flaskSpellChecker/static/underlineWords.js
              //console.log("text: ", text_value)
              //console.log("misspelled: ", data)
              //console.log(text_html)
              // CASE: if there's 1 misspelled and it is canceled, then replace the HTML with the actual text
              if (data.length ==0)
                document.getElementById("textArea").innerHTML=text_value
              else{
                tmp = text_value
                for (let i = 0; i < data.length; i++){
                  word = data.at(i)
                  //console.log("word ", word)
                  tmp = tmp.replace(word, '<span style="text-decoration: underline 2px red;">'+word+'</span>');
                  document.getElementById("textArea").innerHTML=tmp
                  //console.log(tmp)
                }
              }
=======
              console.log(text_value)
              console.log(data)
              tmp = text_value
              for (let i = 0; i < data.length; i++){
                word = data.at(i)
                tmp = tmp.replace(word, '<span style="text-decoration: underline 2px red;">'+word+'</span>');
                document.getElementById("textArea").innerHTML=tmp
                //console.log(tmp)
               }
              
>>>>>>> b83e5839c03a2cc1af8f71fee9064ba652ed1ba7:flaskSpellChecker/static/underlineWords.js
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

      
  
      // Set cursor at the end of text area
      function setEndOfContenteditable(contentEditableElement)
      {
          var range,selection;
          if(document.createRange)//Firefox, Chrome, Opera, Safari, IE 9+
          {
              range = document.createRange();//Create a range (a range is a like the selection but invisible)
              range.selectNodeContents(contentEditableElement);//Select the entire contents of the element with the range
              range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
              selection = window.getSelection();//get the selection object (allows you to change selection)
              selection.removeAllRanges();//remove any selections already made
              selection.addRange(range);//make the range you have just created the visible selection
          }
          else if(document.selection)//IE 8 and lower
          { 
              range = document.body.createTextRange();//Create a range (a range is a like the selection but invisible)
              range.moveToElementText(contentEditableElement);//Select the entire contents of the element with the range
              range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
              range.select();//Select the range (make it the visible selection
          }
      }
  
      });


function GetSelectedText() {
    /*
    Get the text selected on the web page
    */

    if (document.getSelection) {    // all browsers, except IE before version 9
        var sel = document.getSelection();
            // sel is a string in Firefox and Opera, 
            // and a selectionRange object in Google Chrome, Safari and IE from version 9
            // the alert method displays the result of the toString method of the passed object
        //alert(sel);
        return sel.toString()
    } 
    else {
        if (document.selection) {   // Internet Explorer before version 9
            var textRange = document.selection.createRange();
            return textRange.text
        }
    }
}
