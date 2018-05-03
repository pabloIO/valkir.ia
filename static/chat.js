(function(d, io){
    'use strict';

    var io = io.connect('http://localhost:3000'),
        chatForm = d.querySelector('#chat-form'),
        messageText = d.querySelector('#message-text'),
        chat = d.querySelector('#chat');

    chatForm.onsubmit = function(e){
        e.preventDefault();
        io.emit('new message', messageText.value);
        messageText.value=null;
        return false;
    }

    io.on('connect', function(){
        console.log('succesfull python connection');
        io.emit('message', {data: 'CONNECTION JS-PYTHON'})
    });

    io.on('new user', function(newUser){
        alert(newUser.message);
    });

    io.on('user says', function(userSays){
        chat.insertAdjacentHTML('beforeend', '<li>'+userSays+'</li>');
    });

    io.on('bye bye user', function(byeByeUser){
        alert(byeByeUser.message);
    });

})(document, io);