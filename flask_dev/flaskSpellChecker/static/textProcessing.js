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