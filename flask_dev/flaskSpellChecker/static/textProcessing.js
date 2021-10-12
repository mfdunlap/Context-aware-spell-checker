/*
Author: Lorenzo

To include in your html code:
<script src = "{{url_for('static', filename='textProcessing.js')}}"></script>
*/

// Get word by cursor selection
$(document).ready(function() {
    $("#textArea").on('click', function(e) {
        /*var text = document.getElementById("textArea").textContent,
        //var text = $(".clickable").text(),
        element = $("#textArea")[0];
        console.log(text)
        arr = text.split(" ")
        console.log(element.selectionStart)*/
        console.log(GetSelectedText())
        selString = GetSelectedText()
        /*
        arr1 = text.split(" "),
        length = 0,
        selected = arr1[0]
        selectIndex = element.selectionStart;
        console.log(text)
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
      }*/
      // Ajax integration: selected word is forwarded to backend through POST request
        $.ajax({
          type: "POST",
          url : "http://localhost:5000/selected",
          cache: false,
          dataType : "json",
          data : {
              'test': selString
        },
          success : function(suggestions) {
              //alert(data);
              console.log(suggestions);
              //response(suggestions);
          },
        });
  });
});