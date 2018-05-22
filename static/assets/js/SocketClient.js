(function(d, io){
    'use strict';

    var io = io.connect('http://localhost:3000'),
        chatForm = d.querySelector('#chat-form'),
        messageText = d.querySelector('#message-text'),
        chat = d.querySelector('#chat');
    const channel = LocalStorage.getKey('socket_channel');
    console.log(channel);
    io.emit('create_room', {room: channel});

    chatForm.onsubmit = function(e){
        e.preventDefault();
        chat.insertAdjacentHTML('beforeend', '<li>'+messageText.value+'</li>');        
        io.emit('new message', messageText.value);
        messageText.value=null;
        return false;
    }

    io.on('connect', function(){
        console.log('succesfull python connection');  
    });

    io.on('new user', function(newUser){
        alert(newUser.message);
    });

    io.on('user_says:msg', function(data){
        console.log(data);
        chat.insertAdjacentHTML('beforeend', '<li>'+data+'</li>');
    });

    io.on('bye bye user', function(byeByeUser){
        alert(byeByeUser.message);
    });

})(document, io);