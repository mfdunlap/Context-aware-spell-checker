/*
Author: Lorenzo

To include in your html code:
<script src = "{{url_for('static', filename='textProcessing.js')}}"></script>

*/

// Autocomplete function

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


/*
// Get word by cursor selection
//$(document).ready(function() {
    $("#textArea").on('click', function(e) {
        var text = document.getElementById("textArea").value,
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
//});
*/

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
});
*/
