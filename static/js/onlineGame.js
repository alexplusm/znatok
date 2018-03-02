$(document).ready( function() {

	const ws_path = "/waiting_room/";
	const webSocketBridge = new channels.WebSocketBridge();
    let gameIsEnd = false;
    let result = 0;
    var trueAnswer = '';
    var g1 = '';


	$("#btn_for_online_7").click(function () {
	    $(this).addClass("disabled");
	    $("#waitconnection").show();

	    webSocketBridge.connect(ws_path);
	    console.log("Connecting to " + ws_path);


    	webSocketBridge.listen(function(data) {
        // console.log('listen : ', data)

        switch (data.command) {
        	case 0:
        		console.log('CONnect');
        		break;
        	// case 1:
         //        console.log('SUCCESS') 
        	// 	break;
        	case 2:
                console.log('START GAME');
                var questsData = data.quests;
                g1 = new Game(data.quests);

                console.log(g1)
                g1.renderNextQuestion();

                // console.log('TRUUUUUE',questsData.trueAnswer);
                // window.trueAnswer = questsData.trueAnswer
                // var game = new GAME(data.quests)

                // console.log(questsData);
                // insertQuest(questsData, 0);



        		break;
        	case 3:
        		break;
        	case 4:
        		break;			
        		


        }



        });
	});


function insertQuest(data, cnt) {
    console.log('insertQuest', data, cnt);
    document.getElementById('game-quest').innerHTML = data[cnt].question;
    $('.game-img').attr("src", "/media/" + data[cnt].picture);

    document.getElementById('game-answer1').innerHTML = data[cnt].answer1;
    document.getElementById('game-answer2').innerHTML = data[cnt].answer2;

    if (data[cnt].answer2) {
        document.getElementById('game-answer3').innerHTML = data[cnt].answer3;
        $('#game-answer3').show();
    }
    else $('#game-answer3').hide();
    if (data[cnt].answer4) {
        document.getElementById('game-answer4').innerHTML = data[cnt].answer4;
        $('#game-answer4').show();
    }
    else $('#game-answer4').hide();
    if (data[cnt].answer5) {
        document.getElementById('game-answer5').innerHTML = data[cnt].answer5;
        $('#game-answer5').show();
    }
    else $('#game-answer5').hide();
}


$('.game-answbtn').click(function() {
    var userAnswer = $(this).html();
    console.log('game-answbtn');
    if (g1) {
        g1.checkUserAnswer(userAnswer);    
    }
    
});



// var GAME = {
//     gameData: [],
//     gameCNT: 0,

//     constructor(data) {
//         this.gameData = data;
//     };

//     nextQuest() {
//         this.gameCNT += 1;
//     };
// }

function Game(data) {
    this.gameData = data;
    this.gameCNT = 0;
    this.trueAnswer = this.gameData[this.gameCNT].trueAnswer;
    this.result = [];

    this.renderNextQuestion = function() {
        console.log('renderNextQuestion', this.gameData[this.gameCNT], this.gameCNT);
        document.getElementById('game-quest').innerHTML = this.gameData[this.gameCNT].question;
        $('.game-img').attr("src", "/media/" + this.gameData[this.gameCNT].picture);

        document.getElementById('game-answer1').innerHTML = this.gameData[this.gameCNT].answer1;
        document.getElementById('game-answer2').innerHTML = this.gameData[this.gameCNT].answer2;

        if (data[this.gameCNT].answer2) {
            document.getElementById('game-answer3').innerHTML = this.gameData[this.gameCNT].answer3;
            $('#game-answer3').show();
        }
        else $('#game-answer3').hide();
        if (data[this.gameCNT].answer4) {
            document.getElementById('game-answer4').innerHTML = this.gameData[this.gameCNT].answer4;
            $('#game-answer4').show();
        }
        else $('#game-answer4').hide();
        if (data[this.gameCNT].answer5) {
            document.getElementById('game-answer5').innerHTML = this.gameData[this.gameCNT].answer5;
            $('#game-answer5').show();
        }
        else $('#game-answer5').hide();
    }

    this.checkUserAnswer = function(userAnswer) {
      console.log('checkUserAnswer')
      if (userAnswer === this.trueAnswer) {
        this.result.push(1);
      } else {
        this.result.push(0);
      }
      if (this.gameCNT < 9) {
        this.gameCNT += 1;
        this.renderNextQuestion();
      } else {
        this.endGame();
      }
    }
    this.endGame = function() {
      console.log(this.result);
      console.log('endGame');
    }



}


});




















// var generalData = {};
// var userID = document.getElementById('userID').value
// var questID = document.getElementById('questID').value



// $( ".btnd" ).click(function() {
// 	generalData.ddata = $(this).val();
// 	generalData.userid = userID;
// 	generalData.questid = questID
// 	console.log(generalData)
// 	// var str = JSON.stringify(generalData);
//  //    socket.send(str);

// });

// function recieveData() {
// 	var dData = document.getElementById('usData').value;

// 	generalData.ddata = dData
// 	generalData.userid = userID
// 	console.log(generalData)
// 	// var str = JSON.stringify(generalData);
//  //    socket.send(str);
// }






// var server_answer = ' ';
// var user_id = 0;

// function tryConnect() {
   
//     $.ajax({

//             type: "GET",

//             url: "../add/",

//             cache: false,
            
//             success: function(data){
//                 server_answer = data.waiting_room;
//                 user_id = data.user_id;
//                 wait_socket = connectToWaitingRoom(server_answer, user_id);
//                 var str_to_recieve = JSON.stringify({"user_id": user_id, "server_answer": server_answer});
//                 wait_socket.onopen = () => wait_socket.send(str_to_recieve);

                // console.log('connect', server_answer, user_id)

                // проверка - если пользователь зарегистрирован, то открываем сокет
                // if (data.waiting_room === true) {




                //     let socket_url = "ws://" + window.location.host + "/waiting_room/";
                //     wait_socket = new WebSocket(socket_url);
                //     console.log('wait_room_WEBsocket is open!')
                //     window.Notify.generate('Соединениe успешно!','INFO', 0);
                       
                // } else { 
                //     console.log('User not auth or other error');
                //     Notify.generate('Что-то пошло не так','ERROR', 3);
                // }

//             }
//        });



// };


// function connectToWaitingRoom(server_answer, user_id) {
//     if (server_answer == true) {
//         // let socket_url = "ws://" + window.location.host + "/waiting_room/";
//         // wait_socket = new WebSocket(socket_url);
//         // console.log('wait_room_WEBsocket is open!')

//         var ws_path = "/waiting_room/";
//         var webSocketBridge = new channels.WebSocketBridge();
//         webSocketBridge.connect(ws_path);
//         console.log("Connecting to " + ws_path);
//         webSocketBridge.listen(function(data) {
//             console.log('listen : ', data)

//             if (data.command == 0) {
//                 console.log('CONNECT')
//             }
//             if (data.command == 1) {
//                 console.log('SUCCESS')

//                 webSocketBridge.send({
//                     "command":"CLIENT SUCCESS",
//                     "room": data.room,
//                 });
//             }
//             if (data.command == 2) {
//                 console.log('SUCCESS')
//             }
//             if (data.command == 3) {
//                 console.log('SUCCESS')
//             }
//             if (data.command == 4) {
//                 console.log('SUCCESS')
//             }




//         });

//         // trySendMes();
//         window.Notify.generate('Соединениe успешно!','INFO', 0);
//     }
//     // return wait_socket;
// }




// const webSocketBridge = new WebSocketBridge();
// webSocketBridge.connect();
// webSocketBridge.listen(function(action, stream) {
//     console.log(action, stream);
// });

// wait_socket.onopen = function() {
//     console.log('WAIT_WebSocket open')
//     }


// function trySendMes() {

//     var strasd = JSON.stringify({"mess":"answCode"});
//     wait_socket.send(strasd);

// }






Notify = {              
    TYPE_INFO: 0,               
    TYPE_SUCCESS: 1,                
    TYPE_WARNING: 2,                
    TYPE_DANGER: 3,                             

    generate: function (aText, aOptHeader, aOptType_int) {                  
        var lTypeIndexes = [this.TYPE_INFO, this.TYPE_SUCCESS, this.TYPE_WARNING, this.TYPE_DANGER];                    
        var ltypes = ['alert-info', 'alert-success', 'alert-warning', 'alert-danger'];                                      
        var ltype = ltypes[this.TYPE_INFO];                 

        if (aOptType_int !== undefined && lTypeIndexes.indexOf(aOptType_int) !== -1) {                      
            ltype = ltypes[aOptType_int];                   
        }                                       

        var lText = '';                 
        if (aOptHeader) {                       
            lText += "<h4>"+aOptHeader+"</h4>";                 
        }                   
        lText += "<p>"+aText+"</p>";                                        
        var lNotify_e = $("<div class='alert "+ltype+"'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>×</span></button>"+lText+"</div>");                    

        setTimeout(function () {                        
            lNotify_e.alert('close');                   
        }, 3000);                   
        lNotify_e.appendTo($("#notifies"));             
    }           
};  

