/*
Author: Lorenzo

To include in your html code:
<script src = "{{url_for('static', filename='textProcessing.js')}}"></script>

*/

// Autocomplete function
/*
$(document).ready(function() {
    $("#textArea").autocomplete({
        source : function(request, response) {
            $.ajax({
                type: "POST",
                url : "http://localhost:5000/",
                dataType : "json",
                cache: false,
                data : {
                    'text' : request.term
                },
                success : function(data) {
                    //alert(data);
                    //console.log(data);
                    response(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log(textStatus + " " + errorThrown);
                }
            });
        },
        minLength : 2
    });
});
*/

/*
// Get word by cursor selection
//$(document).ready(function() {
    $("#textArea").on('click', function(e) {
        //var text = document.getElementById("textArea").value,
        var text = $("textArea").text(),
        element = $("#textArea")[0],
        arr1 = text.split(" "),
        length = 0,
        selectIndex = element.selectionStart;
        //console.log(selectIndex);
      if (selectIndex == 0){
        //console.log(arr1.indexOf(arr1[0]));
        selected = arr1[0]
        console.log(arr1[0]);
      }
      else {
        for (var i = 0; i < arr1.length; i++) {            
          length = length + arr1[i].length + 1;
          if (length == selectIndex) {
            selected = arr1[i+1]
            console.log(arr1[i + 1]);
            break;
          }
        }
      }
      // Ajax integration: selected word is forwarded to backend through POST request
        $.ajax({
          type: "POST",
          url : "http://localhost:5000/",
          cache: false,
          dataType : "json",
          data : {'data': selected},
          success : function(suggestions) {
              //alert(data);
              //console.log(data);
              response(suggestions);
          },
        });
  });
*/

// Send text fo backend and return misspelled word for underlining
/*
$(document).ready(function() {
  document.getElementById("textArea").onkeyup = function(){
  
    // Get the text from text area
    var text_value = document.getElementById("textArea").value;
    //console.log(text_value.at(-1))

    
    if (text_value.at(-1) === " ") {
      console.log("test")
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
            
            //for (let i = 0; i < data.length; i++){
            //  underlinedText = text_value.replace(/(nams)/gi, '<b>$1</b>');
            //  console.log(underlinedText)
            //  document.getElementById("textArea").value=underlinedText
            //  }
            

            //$("textArea").css('text-decoration','underline')
            underlinedText = text_value.replace(/(nams)/gi, '<span>$1</span>');
            console.log(underlinedText)
            document.getElementById("textArea").value=underlinedText
            //$("#textArea").value = underlinedText.css('text-decoration', 'underline')
            
              //alert(data);
              //console.log(data);
              //response(data);
          },
        //error: function(jqXHR, textStatus, errorThrown) {
        //    console.log(textStatus + " " + errorThrown);
        //}
      });

      //document.getElementById('warning_text').innerHTML = "You are using the forbidden word";
    } else {
      //console.log("none")
      //document.getElementById('warning_text').innerHTML = "";
    }

   
 
 };
});
*/

//});


  // Get word by passing the cursor on it
  /*
  $(document).ready(function() {
    // wrap words in spans
    $('p').each(function() {
        var $this = $(this);
        $this.html($this.text().replace(/\b(\w+)\b/g, "<span>$1</span>"));
    });

    // bind to each span
    $('p span').hover(
        function() { $('#word').text($(this).css('background-color','#ffff66').text()); },
        function() { $('#word').text(''); $(this).css('background-color',''); }
    );
});*/

// Underline misspelled words
$(document).ready(function(){
  document.getElementById("textArea").onkeyup = function(){
    //var text_value = document.getElementById("textArea");
    text_value = $("#textArea").text();

    text_html= document.getElementById("textArea");
    text_html = text_html.innerHTML

    console.log(text_value.at(-1))
    
    if(text_html.at(-1) === ';') {
      console.log("space detected");
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
            console.log(data)
            tmp = text_value
            for (let i = 0; i < data.length; i++){
              word = data.at(i)
              tmp = tmp.replace(word, '<span style="background-color:yellow">'+word+'</span>');
              document.getElementById("textArea").innerHTML=tmp
              //underlinedText = text_value.replace(/(nams)/gi, '<u>$1</u>');
              console.log(tmp)
             }
            

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
