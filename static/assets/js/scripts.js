
//funcion captura de nombre de usuario y envio a mediante de petición ajax
function login(){
    objetoVariables = {
        username: $('#txt_user_name').val()
    }
    login = ajaxPeticionJS('POST', 'http://localhost:3000/login', objetoVariables);
    console.log(login);
}

//Funcion ajax reutilizable
function ajaxPeticionJS(metodo, ruta, request = []){
    // alert(request);
    var resultado;
    $.ajax({
        type: metodo,
        url : ruta,
        data : request,
        success :            
            function(resul){
                resultado = resul;
            }
    });
    return resultado;
}