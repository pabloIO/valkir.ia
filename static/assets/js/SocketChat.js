$(function() {
    var FADE_TIME = 150; // ms
    var TYPING_TIMER_LENGTH = 400; // ms
    var COLORS = [
      '#e21400', '#91580f', '#f8a700', '#f78b00',
      '#58dc00', '#287b00', '#a8f07a', '#4ae8c4',
      '#3b88eb', '#3824aa', '#a700ff', '#d300e7'
    ];
  
    // Initialize varibles
    var $window = $(window);
    var $messages = $('#messages'); // Messages area
    var $inputMessage = $('.inputMessage'); // Input message input box
  
    var $loginPage = $('.login.page'); // The login page
    var $chatPage = $('.chat.page'); // The chatroom page
    ////////////////////INICIO////////////////////
    var $titleLogin = $('.title');
    var form = $('.form-chat');
    ///////////////////  FIN  ///////////////////
  
    // Prompt for setting a userName
    var user_conversation = [];
    var connected = true;
    var typing = false;
    var lastTypingTime;
    // var $currentInput = $userNameInput.focus();
    
    var socket = io('http://localhost:3000');
    var channel = LocalStorage.getKey('socket_channel');
    var userName = LocalStorage.getKey('username');
    var sesion_id = LocalStorage.getKey('sesion');
    var _conversation_id = LocalStorage.getKey('_conversation_id');
    var user_id = LocalStorage.getKey('id');
    getConversation(user_id);
    // console.log(userName)
    // console.log(`joining to room ${channel}`);
    socket.emit('create_room', {room: channel});
    socket.emit('add_user', {usr: userName});

    socket.on('connect', function(){
        console.log('succesfull python connection');    
    });
    

    function getConversation(id){
      // alert(request);
      let user_id = id;
      var conv = null;
      $.ajax({
          method: 'GET',
          url : `http://localhost:3000/user/${user_id}/conversation`,
          async: false,
          success: function(response){
                if(response.success){
                // conversation = response.conversation;

                user_conversation = response.conversation;
                for (let i = 0; i < user_conversation.length; i++) {
                  addChatMessage(user_conversation[i].user_res);
                  addChatMessage(user_conversation[i].bot_res);
                }
            }else{
                alert(response.msg);
            }
          }
      });
    }

    function addParticipantsMessage (data) {
      var message = '';
      if (data.numUsers === 1) {
        message += "Ahora 1 participante";
      } else {
        message += "Ahora " + data.numUsers + " participantes";
      }
      log(message);
    }
  
    // Sets the client's userName
    function setuserName () {
      userName = cleanInput($userNameInput.val().trim());
      // If the userName is valid
  
      ////////////////////INICIO////////////////////
      if (userName) {
        socket.emit('exists user', userName, function (cbValue){
          if(cbValue)
          {
            $loginPage.fadeOut();
            $chatPage.show();
            $loginPage.off('click');
            $currentInput = $inputMessage.focus();
  
            // Tell the server your userName
            socket.emit('add_user', userName);
          }
          else
          {
            $titleLogin.html('The user "' + userName + '" already exists!');
            $userNameInput.val(null);
            userName = null;
          }
        })
      }
      ///////////////////  FIN  ///////////////////
      
      /*
      Original Code
      if (userName) {
        $loginPage.fadeOut();
        $chatPage.show();
        $loginPage.off('click');
        $currentInput = $inputMessage.focus();
  
        // Tell the server your userName
        socket.emit('add user', userName);
      }
      */
    }
  
    // Sends a chat message
    function sendMessage () {
      var message = $inputMessage.val();

      // Prevent markup from being injected into the message
      message = cleanInput(message);
      // if there is a non-empty message and a socket connection
      if (message && connected) {
        $inputMessage.val('');
        addChatMessage({
          userName: userName,
          message: message
        });
        // tell server to execute 'new message' and send along one parameter
        socket.emit('new_message', {
          message: message,
          room: channel,
          _conversation_id: _conversation_id,
          sesion_id: sesion_id,
          user_id: user_id,
        });
      }
    }
  
    // Log a message
    function log (message, options) {
      var $el = $('<li>').addClass('log').text(message);
      addMessageElement($el, options);
    }
  
    // Adds the visual chat message to the message list
    function addChatMessage (data, options) {
      // Don't fade the message in if there is an 'X was typing'
      var $typingMessages = getTypingMessages(data);
      options = options || {};
      if ($typingMessages.length !== 0) {
        options.fade = false;
        $typingMessages.remove();
      }
  
      var $userNameDiv = $('<span class="username"/>')
        .text(data.userName)
        .css('color', getuserNameColor(data.userName));
      var $messageBodyDiv = $('<span class="messageBody">')
        .text(data.message);
  
      var typingClass = data.typing ? 'typing' : '';
      var $messageDiv = $('<li class="message"/>')
        .data('username', data.userName)
        .addClass(typingClass)
        .append($userNameDiv, $messageBodyDiv);
  
      addMessageElement($messageDiv, options);
    }
  
    // Adds the visual chat typing message
    function addChatTyping (data) {
      data.typing = true;
      data.message = 'está escribiendo';
      addChatMessage(data);
    }
  
    // Removes the visual chat typing message
    function removeChatTyping (data) {
      getTypingMessages(data).fadeOut(function () {
        $(this).remove();
      });
    }
  
    // Adds a message element to the messages and scrolls to the bottom
    // el - The element to add as a message
    // options.fade - If the element should fade-in (default = true)
    // options.prepend - If the element should prepend
    //   all other messages (default = false)
    function addMessageElement (el, options) {
      var $el = $(el);
      // Setup default options
      if (!options) {
        options = {};
      }
      if (typeof options.fade === 'undefined') {
        options.fade = true;
      }
      if (typeof options.prepend === 'undefined') {
        options.prepend = false;
      }
  
      // Apply options
      if (options.fade) {
        $el.hide().fadeIn(FADE_TIME);
      }
      if (options.prepend) {
        $messages.prepend($el);
      } else {
        $messages.append($el);
      }
      $messages[0].scrollTop = $messages[0].scrollHeight;
    }
  
    // Prevents input from having injected markup
    function cleanInput (input) {
      return $('<div/>').text(input).text();
    }
  
    // Updates the typing event
    function updateTyping () {
      if (connected) {
        if (!typing) {
          typing = true;
          socket.emit('typing', {
            userName: userName,
            room: channel});
        }
        lastTypingTime = (new Date()).getTime();
  
        setTimeout(function () {
          var typingTimer = (new Date()).getTime();
          var timeDiff = typingTimer - lastTypingTime;
          if (timeDiff >= TYPING_TIMER_LENGTH && typing) {
            socket.emit('stop typing', {
              userName: userName,
              room: channel
            });
            typing = false;
          }
        }, TYPING_TIMER_LENGTH);
      }
    }
  
    // Gets the 'X is typing' messages of a user
    function getTypingMessages (data) {
      return $('.typing.message').filter(function (i) {
        return $(this).data('userName') === data.userName;
      });
    }
  
    // Gets the color of a userName through our hash function
    function getuserNameColor (userName) {
      // Compute hash code
      var hash = 7;
      for (var i = 0; i < userName.length; i++) {
         hash = userName.charCodeAt(i) + (hash << 5) - hash;
      }
      // Calculate color
      var index = Math.abs(hash % COLORS.length);
      return COLORS[index];
    }
  
    // Keyboard events
    form.submit(function(evt){
      evt.preventDefault();
      sendMessage();
      socket.emit('stop typing', {
        userName: userName,
        room: channel
      });
    });
    
    // $window.keydown(function (event) {
      // Auto-focus the current input when a key is typed
      // if (!(event.ctrlKey || event.metaKey || event.altKey)) {
      //   $currentInput.focus();
      // }
      // When the client hits ENTER on their keyboard
      // console.log(userName);
      // if (event.which === 13) {
      //   alert("Enter");
      //   if (userName) {
      //     sendMessage();
      //     socket.emit('stop typing');
      //     typing = false;
      //   } else {
      //     setuserName();
      //   }
      // }
    // });
  
    $inputMessage.on('input', function() {
      updateTyping();
    });
  
    // Click events
  
    // Focus input when clicking anywhere on login page
    $loginPage.click(function () {
      $currentInput.focus();
    });
  
    // Focus input when clicking on the message input's border
    $inputMessage.click(function () {
      $inputMessage.focus();
    });
  
    // Socket events
  
    // Whenever the server emits 'login', log the login message
    socket.on('login', function (data) {
      // Display the welcome message
      var message = "Bienvenido a la sala de Chat Valkiria";
      log(message, {
        prepend: true
      });
      addParticipantsMessage(data);
    });
  
    // Whenever the server emits 'new message', update the chat body
    socket.on('user_says:msg', function (data) {
      addChatMessage(data);
    });
  
    // Whenever the server emits 'user joined', log it in the chat body
    socket.on('user_joined', function (data) {
        // alert(`El usuario ${data.userName} ha entrado a la sala de chat`);
        log(`${data.username} se ha conectado`);
        addParticipantsMessage(data);
    });
  
    // Whenever the server emits 'user left', log it in the chat body
    socket.on('user_left', function (data) {
      log(data.userName + ' Desconectado');
      addParticipantsMessage(data);
      removeChatTyping(data);
    });
  
    // Whenever the server emits 'typing', show the typing message
    socket.on('typing', function (data) {
      addChatTyping(data);
    });
  
    // Whenever the server emits 'stop typing', kill the typing message
    socket.on('stop typing', function (data) {
      removeChatTyping(data);
    });

    socket.on('reconnect', function(){
      // log('you have been reconnected');
      if (userName) {
        socket.emit('create_room', {room: channel});        
        socket.emit('add_user', {usr: userName});
      }
    });
  });
  