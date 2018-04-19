
function httpGet(theUrl)
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
        changeDropdownVals(array_data)
    });
}

function changeDropdownVals(options){

    var sel = document.getElementById('functionName');
    for(var i = 0; i < options.length; i++) {
        var opt = document.createElement('option');
        opt.innerHTML = options[i];
        opt.value = options[i];
        sel.appendChild(opt);
    }
}

function onFunctionNameLoad()
{
    var url = "http://127.0.0.1:3034/getFunctionName"
    options = httpGet(url)
}

function checkFile()
{
    if(document.getElementById("inputFunctionFile").value != "") {
       alert("Selected the file");
       return true
    }
    else{
        alert("Please select a file first");
        return false
    }
}
