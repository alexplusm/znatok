$(document).ready( function() {

	const ws_path = "/waiting_room/";
	const webSocketBridge = new channels.WebSocketBridge();
    let gameIsEnd = false;
    let result = 0;
    var trueAnswer = '';
    var game = '';

    let requestToServer = {
        command: 'comm',
        user: 'user',
        group: 'group',
        result: 'result'
    }

    /*  
    *  Список команд на сервер:
    *
    *
    */

    // TO SEND
    // webSocketBridge.send({prop1: 'value1', prop2: 'value1'});

    // JSON ответа:
    // {command: 'comm', user: 'user', group: 'group', result: 'result'}




    // Click on 'Start game' button

	$("#btn_for_online_7").click(function () {
	    $(this).addClass("disabled");
	    $("#waitconnection").show();

	    webSocketBridge.connect(ws_path);
	    console.log("Connecting to " + ws_path);

    	webSocketBridge.listen(function(data) {
        console.log('listen WS: ', data)

        switch (data.command) {
        	case 0:
        		console.log('CONNECT');
        		break;
        	// case 1:
         //        console.log('SUCCESS') 
        	// 	break;
        	case 2:
                console.log('START GAME');
                var questsData = data.quests;
                game = new Game(data.quests);
                game.startGame();
        		break;
        	case 3:
            // END GAME => SHOW RESULTS
        		break;
        	case 4:
        		break;			
        		
        }

        });
	});



    $('.game-answbtn').click(function() {
        var userAnswer = $(this).html();
        console.log('game-answbtn');
        if (game) {
            game.checkUserAnswer(userAnswer);    
        }
    });



    function Game(data) {
        this.gameData = data;
        this.gameCNT = 0;
        this.trueAnswer = this.gameData[this.gameCNT].trueAnswer;
        this.result = [];

        this.startGame = function() {
            this.gameCNT = 0;
            this.renderNextQuestion();
        }

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
            let countOfRightAnswers = this.result.reduce((count, item) => {
                if (item === 1) { count += 1; }
                return count;   
            })
            console.log('COUNT OF RIGHT ANSWERS', countOfRightAnswers);
            requestToServer.command = 'END_GAME'
            webSocketBridge.send(requestToServer);

        }
    }


});











// function insertQuest(data, cnt) {
//     console.log('insertQuest', data, cnt);
//     document.getElementById('game-quest').innerHTML = data[cnt].question;
//     $('.game-img').attr("src", "/media/" + data[cnt].picture);

//     document.getElementById('game-answer1').innerHTML = data[cnt].answer1;
//     document.getElementById('game-answer2').innerHTML = data[cnt].answer2;

//     if (data[cnt].answer2) {
//         document.getElementById('game-answer3').innerHTML = data[cnt].answer3;
//         $('#game-answer3').show();
//     }
//     else $('#game-answer3').hide();
//     if (data[cnt].answer4) {
//         document.getElementById('game-answer4').innerHTML = data[cnt].answer4;
//         $('#game-answer4').show();
//     }
//     else $('#game-answer4').hide();
//     if (data[cnt].answer5) {
//         document.getElementById('game-answer5').innerHTML = data[cnt].answer5;
//         $('#game-answer5').show();
//     }
//     else $('#game-answer5').hide();
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

