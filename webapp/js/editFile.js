
function httpGet(theUrl)
{
     var request = $.ajax({
        type: "POST",
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
