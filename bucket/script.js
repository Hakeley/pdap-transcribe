let API_URL = "{INSERT YOUR API_URL HERE}"

function warning(msg){
        document.getElementById("announcement").style.display = "block";
        document.getElementById("announcement").innerHTML = msg;
}

$( document ).ajaxError(function( event, request, settings ) {
$( "#msg" ).append( "<li>Error requesting page " + settings.url + "</li>" );
});

$(document).ready(function () {
    // filereader api to convert JSON file to string
    var fr = new FileReader();



    $('#submit').click(function(){
        // if file is chosen, input:valid length is 1; else 0
        elt = document.getElementById("json_file");
        console.log(elt);
        if (jQuery('input:valid').length == 1){
          document.getElementById("loading_img").style.display = "block";
          $.ajax({
            type: "POST",
            url: API_URL,
            crossDomain: true,
            data: fr.result, //data has to be string or throws CORS error
            contentType: "application/json",
            dataType: "json",
            success: function(data, status){
              console.log(data);
              if (data.errorMessage !== undefined){
                // If reached here, probably gave unexpected input that broke the python script
                if (data.errorMessage.match("timed out") !== null){
                    warning("Task timed out.")
                }
                else{
                    warning("File content isn't as expected.")
                }

              }
              else{
                //Gets a good response back from lambda
                document.getElementById("announcement").style.display = "none";
                document.getElementById('DOWNLOAD').click();
              }
            }
        }).fail(function (data) {
            warning("Wrong filetype.") //Gives CORS error and reaches here if lambda doesn't give a response back.
        }).always( function(){
            document.getElementById("loading_img").style.display = "none";
            });
        };
      });

    // When file is chosen, read it immediately
    $("#json_file").change(function handleFileSelect()
    {
      if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
        alert('The File APIs are not fully supported in this browser.');
        return;
      }
      var input = document.getElementById('json_file');
      if (!input) {
        alert("Um, couldn't find the fileinput element.");
      }
      else if (!input.files) {
        alert("This browser doesn't seem to support the `files` property of file inputs.");
      }
      else if (!input.files[0]) {
        alert("Please select a file before clicking 'Load'");
      }
      else {
        var file = input.files[0];
        fr.readAsText(file);
      }
    });
  });
