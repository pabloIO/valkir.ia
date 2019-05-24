
//funcion captura de nombre de usuario y envio a mediante de petición ajax
function login(){
    objetoVariables = {
        username: $('#txt_user_name').val()
    }
    ajaxPeticionJS('POST', 'http://192.168.0.107:3000/login', objetoVariables);
}


//Funcion ajax reutilizable
function ajaxPeticionJS(metodo, ruta, request = []){
    // alert(request);
    $.ajax({
        method: metodo,
        url : ruta,
        data : request,
    })
    .done(function(response){
        if(response){
            LocalStorage.setKeys(response);
            window.location.href = response.url_to;
        }
    });
}
