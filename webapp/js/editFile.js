


function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function changeDropdownVals(options){

    var cuisines = ["Chinese","Indian"];

    var sel = document.getElementById('functionName');
    for(var i = 0; i < cuisines.length; i++) {
        var opt = document.createElement('option');
        opt.innerHTML = cuisines[i];
        opt.value = cuisines[i];
        sel.appendChild(opt);
    }
}


function onFunctionNameLoad()
{
    var url = "http://127.0.0.1:3034/getFunctionName"
    options = httpGet(url)
    changeDropdownVals(options)
}
