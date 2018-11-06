'use strict';

angular.module('chatDialog').
	component('chatDialog',{
		templateUrl :'api/templates/chat/chat_dialog.html',
	// template:"<ng-include src='getTemplateUrl()'/>",
		controller : function($scope,$http,$routeParams,$mdToast,$cookies,$rootScope,$cookieStore){
        
		var username=$routeParams.username

		$scope.username=$routeParams.username
		$scope.main_user=$cookies.get('username')
        var main_user=$cookies.get('username')
		var url = 'api/chat/dialogs/'+username+''
		var req = {
			url:url ,
			method : 'GET',				
			isArray:true,
			
		}

			var reqResp = $http(req)

        	reqResp.success(function(r_data,r_status,r_headers,r_config){
        		$scope.messages=r_data
        		console.log(r_data)
        		
        		             		
    })
      reqResp.error(function(e_data,e_status,e_headers,e_config){
        		console.log(e_data)
                            
        	})
        
 	


     var base_ws_server_path = "ws://localhost:5002/";
        $(document).ready(function () {
            var websocket = null;
            var monitor = null;

            function initReadMessageHandler(containerMonitor, elem) {
                var id = $(elem).data('id');
                var elementWatcher = containerMonitor.create(elem);
                elementWatcher.enterViewport(function () {
                    var opponent_username = getOpponnentUsername();
                    var packet = JSON.stringify({
                        type: 'read_message',
                        session_key: session_key,
                        username: opponent_username,
                        message_id: id
                    });
                    $(elem).removeClass('msg-unread').addClass('msg-read');
                    websocket.send(packet);
                });
            }

            function initScrollMonitor() {
                var containerElement = $("#messages");
                var containerMonitor = scrollMonitor.createContainer(containerElement);
                $('.msg-unread').each(function (i, elem) {
                    if ($(elem).hasClass('opponent')){
                        initReadMessageHandler(containerMonitor, elem);
                    }

                });
                return containerMonitor
            }

            function getOpponnentUsername() {
            	var username=$routeParams.username
                return username;
            }

            // TODO: Use for adding new dialog
            function addNewUser(packet) {
                $('#user-list').html('');
                packet.value.forEach(function (userInfo) {
                    if (userInfo.username == getUsername()) return;
                    var tmpl = Handlebars.compile($('#user-list-item-template').html());
                    $('#user-list').append(tmpl(userInfo))
                });
            }

            function addNewMessage(packet) {
                var msg_class = "";
                

                var main_user = $cookies.get('username');
                
                if (packet['sender_name'] == $("#owner_username").val()) {
                    msg_class = "pull-left";
                } else {
                    msg_class = "pull-right";
                    window.id = packet['message_id']

                    send_seen_msg(id)
                }
                var msgElem_right =
                    $('<div class="row" >' +
                        '<p class="' + msg_class +'">' +                         
                        packet['message'] +
                        ' <span class="timestamp"><span data-livestamp="' + packet['created'] + '"> ' + packet['created'] + 
                         '<span class="unseen" data-id="' + packet.message_id + '">' + '<img src="media/svg/sent.svg" class="unseen_img unseen">' + '</span>' + '</span></span> ' +
                        '</p> ' +
                        '</div>');
                var msgElem_left =
                    $('<div class="row" >' +
                        '<p class="' + msg_class +'">' +                         
                        packet['message'] +
                        ' <span class="timestamp"><span data-livestamp="' + packet['created'] + '"> ' + packet['created'] + 
                         '<span  data-id="' + packet.message_id + '">' + '</span>' + '</span></span> ' +
                        '</p> ' +
                        '</div>');
                if(packet['sender_name'] == $("#owner_username").val()) {
                   $('#messages').append(msgElem_right); 
                }
                else{
                    $('#messages').append(msgElem_left);
                }
                
                scrollToLastMessage()
            }


            function send_seen_msg(elem, packet){ 
                $scope.id = window.id
                console.log($scope.id)

                var opponent_username = getOpponnentUsername();   
                var seen_packet = JSON.stringify({
                    type: 'seen_unseen',
                    session_key: session_key,
                     username: opponent_username,
                    seen: true,
                    message_id: id
               
            });
                websocket.send(seen_packet);
                console.log(seen_packet)

            }
            function scrollToLastMessage() {
                var $msgs = $('#messages');
                $msgs.animate({"scrollTop": $msgs.prop('scrollHeight')})
            }

            function generateMessage(context) {
                var tmpl = Handlebars.compile($('#chat-message-template').html());
                return tmpl({msg: context})
            }

            function setUserOnlineOffline(username, online) {
                var elem = $("#user-" + username);
                if (online) {
                    elem.attr("class", "btn btn-success");
                } else {
                    elem.attr("class", "btn btn-danger");
                }
            }

            function gone_online() {
                $("#offline-status").hide();
                $("#online-status").show();
            }

            function gone_offline() {
                $("#online-status").hide();
                $("#offline-status").show();
            }

            function flash_user_button(username) {
                var btn = $("#user-" + username);
                btn.fadeTo(700, 0.1, function () {
                    $(this).fadeTo(800, 1.0);
                });
            }

            function setupChatWebSocket() {
                var opponent_username = getOpponnentUsername();
                websocket = new WebSocket(base_ws_server_path + session_key1 + opponent_username);

                websocket.onopen = function (event) {
                    var opponent_username = getOpponnentUsername();

                    var onOnlineCheckPacket = JSON.stringify({
                        type: "check-online",
                        session_key: session_key,
                        username: opponent_username
                        // {#                      Sending username because the user needs to know if his opponent is online #}
                    });
                    var onConnectPacket = JSON.stringify({
                        type: "online",
                        session_key: session_key,
                        username: opponent_username

                    });

                    console.log('connected, sending:', onConnectPacket);
                    websocket.send(onConnectPacket);
                    console.log('checking online opponents with:', onOnlineCheckPacket);
                    websocket.send(onOnlineCheckPacket);
                    monitor = initScrollMonitor();
                };


                window.onbeforeunload = function () {

                    var onClosePacket = JSON.stringify({
                        type: "offline",
                        session_key: session_key,
                        username: opponent_username,
                        // {# Sending username because to let opponnent know that the user went offline #}
                    });
                    console.log('unloading, sending:', onClosePacket);
                    websocket.send(onClosePacket);
                    websocket.close();
                };


                websocket.onmessage = function (event) {
                    var packet;

                    try {
                        packet = JSON.parse(event.data);
                        console.log(packet)
                    } catch (e) {
                        console.log(e);
                    }

                    scrollToLastMessage(); 
                    switch (packet.type) {
                        case "new-dialog":
                            // TODO: add new dialog to dialog_list
                            break;
                        case "user-not-found":
                            // TODO: dispay some kind of an error that the user is not found
                            break;
                        case "gone-online":
                            var main_user=$cookies.get('username')
                        	if(packet.chat_with==main_user){
                        		$(".unseen").html('<img src="media/svg/received.svg" class="unseen_img unseen">');
                        		
                        	}
                            if (packet.usernames.indexOf(opponent_username) != -1) {
                                gone_online();
                            } else {
                                gone_offline();
                            }
                            for (var i = 0; i < packet.usernames.length; ++i) {
                                setUserOnlineOffline(packet.usernames[i], true);
                            }
                            break;
                        case "gone-offline":
                            if (packet.username == opponent_username) {
                                gone_offline();
                            }
                            setUserOnlineOffline(packet.username, false);
                            break;
                        case "new-message":
                        	var opponent_username = getOpponnentUsername()
                            var username = packet['sender_name'];
                            var main_user=$cookies.get('username')
                           if (username == opponent_username || username == main_user){
                                addNewMessage(packet);
                                // if (username == opponent_username) {
                                //     initReadMessageHandler(monitor, $("div[data-id='" + packet['message_id'] + "']"));
                                // }
                            } else {
                                if ($("#user-"+username).length == 0){
                                    var new_button = $(''+
                                        '<a href="/'+ username + '"' +
                                        'id="user-'+username+'" class="btn btn-danger">{% trans "Chat with" %} '+username+'</a>');
                                    $("#user-list-div").find("ul").append()
                                }

                                flash_user_button(username);

                                	$mdToast.show(
				                    $mdToast.simple()
				                    .parent(document.querySelectorAll('#toaster'))
                                    .position('top left')
				                    .textContent("You Have New Msg From"+' '+ packet['sender_name'])
				                    .position('top')
				                   
				                    .hideDelay(5000)
				                );

                            }
                            break;
                        case "opponent-typing":
                            var typing_elem = $('#typing-text');
                            if (!typing_elem.is(":visible")) {
                                typing_elem.fadeIn(500);
                            } else {
                                typing_elem.stop(true);
                                typing_elem.fadeIn(0);
                            }
                            typing_elem.fadeOut(3000);
                            break;
                        case "seen_unseen":
                        	var opponent_username = getOpponnentUsername();
                            if (packet['username'] == opponent_username) {
                                $("span[data-id='" + packet['message_id'] + "']").html('<img src="media/svg/received.svg" class="unseen_img unseen">');
                            }
                            
                            break;

                        default:
                            console.log('error: ', event)
                    }
                }
            }

            function sendMessage(message) {
                var opponent_username = getOpponnentUsername();
                var newMessagePacket = JSON.stringify({
                    type: 'new-message',
                    session_key: session_key,
                    username: opponent_username,
                    message: message
                });
                websocket.send(newMessagePacket)
            }
 
            $('#chat-message').keypress(function (e) {
                if (e.which == 13 && this.value) {
                    sendMessage(this.value);
                    this.value = "";
                    return false
                } else {
                    var opponent_username = getOpponnentUsername();
                    var packet = JSON.stringify({
                        type: 'is-typing',
                        session_key: session_key,
                        username: opponent_username,
                        typing: true
                    });
                    websocket.send(packet);
                }
            });

            $('#btn-send-message').click(function (e) {
                var $chatInput = $('#chat-message');
                var msg = $chatInput.val();
                if (!msg) return;
                sendMessage($chatInput.val());
                $chatInput.val('')
            });

            setupChatWebSocket();
            scrollToLastMessage();
        });

}
}
)