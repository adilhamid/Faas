
function httpGet(theUrl, id)
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
        changeDropdownVals(array_data, id)
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
}

function onFunctionNameLoad()
{
    var url = "http://127.0.0.1:3034/getFunctionName"
    options = httpGet(url, 'functionName')
}

function onTopicsLoad()
{
    var url = "http://127.0.0.1:3034/getTopicNames"
    options = httpGet(url, 'kafkaTopic')
}
