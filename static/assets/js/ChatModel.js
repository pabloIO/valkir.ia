'use strict';
var ChatModel = (function(){
    /**
     * @keys: [id, username, token, socket_channel, _conversation_id, sesion]
     */ 
    let conversation = [];
    let _storage = LocalStorage;

    function getConversation(id){
        // alert(request);
        let user_id = id;
        var conv = null;
        $.ajax({
            method: 'GET',
            url : `http://localhost:3000/user/${user_id}/conversation`,
            async: false,
            success: function(response){
                if(response){
                    // conversation = response.conversation;
                    conv = response.conversation;
                }else{
                    alert(response.msg);
                }
            }
        });
    }

    return{
        getConversation: getConversation,
    };
})();

