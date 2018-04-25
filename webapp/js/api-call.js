
function httpGet(theUrl, id, type)
{
     var request = $.ajax({
        type: "GET",
        url: theUrl,
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        data: {"name":""},
        dataType: "html"
    });

    request.done(function(JSON_array) {
        array_data = JSON.parse(JSON_array)["array"]
        if(type === 'dropdown') {
            changeDropdownVals(array_data, id);
        } else if(type === 'table') {
            createTable(array_data, id);
        }
    });
}

function changeDropdownVals(options, id){

    var sel = document.getElementById(id);
    for(var i = 0; i < options.length; i++) {
        var opt = document.createElement('option');
        opt.innerHTML = options[i];
        opt.value = options[i];
        sel.appendChild(opt);
    }

    return true;
}

function createTable(data, id) {

   rows = "<h1 style='text-align: left;'>Output Logs</h1>"
   rows += "<table class='table table-striped'>";
   rows += "<thead>";
   rows += "<tr><th scope='col'><center><b>Timestamp</th><th scope='col'><center><b>Function Name</th><th scope='col'><center><b>User Data</th><th scope='col'><center><b>Result</th></tr>"
   rows += "</thead>";
   rows += "<tbody>";
   for (var event in data) {
      rows += "<tr>";
      rows += "<td>" + data[event].timestamp + "</td>";
      rows += "<td>" + data[event].functionName + "</td>";
      rows += "<td>" + data[event].userData + "</td>";
      rows += "<td>" + data[event].outputResult + "</td>";
      rows += "</tr>";
   }
   rows += "</tbody>";
   rows += "</table>";
   document.getElementById(id).innerHTML = rows;

   return true;
}

function onFunctionNameLoad()
{
    var url = "http://127.0.0.1:3034/getFunctionName"
    options = httpGet(url, 'functionName', 'dropdown')
}

function onTopicsLoad()
{
    var url = "http://127.0.0.1:3034/getTopicNames"
    options = httpGet(url, 'kafkaTopic', 'dropdown')
}

function viewOutputs()
{
    var url = "http://127.0.0.1:3034/getFunctionOutput"
    options = httpGet(url, 'outputlogs', 'table')
}