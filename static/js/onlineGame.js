$(document).ready( function() {

	const ws_path = "/waiting_room/";
	const webSocketBridge = new channels.WebSocketBridge();
    let userId = 0;
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
    *  LIST COMMANDS TO SERVER:
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
                userId = data.userId;
                console.log('CONNECT id=', userId);
        		break;
        	case 1:
                console.log('SUCCESS') 
        		break;
        	case 2:
                // Start game!
                game = new Game(data.quests);
                game.start();
        		break;
        	case 3:
            // END GAME => SHOW RESULTS
        		break;
        	case 4:
        		break;			
        		
        }

        });
	});

    // обработчик конопок ответов в игре
    $('.game-answbtn').click(function() {
        let userAnswer = $(this).html();
        console.log('юзер кликнул на game-answbtn');
        if (game.isActive) {
            game.checkUserAnswer(userAnswer);    
        }
    });


    class Game {
        /* 
        *  this.data - json с набором вопрос с бэкенда
        *  this.count - номер отрендеренного вопроса
        *  this.trueAnswer - после каждого рендера вопроса тут 
        *       хранится правильный ответ для актуального вопроса
        *  this.result - массив с ответами юзера (0 - неправильно, 1 - правильно)
        */
        constructor(data) {
            this.data = data;
            this.count = 0;
            this.trueAnswer = data[0].trueAnswer;
            this.result = [];
            this.isActive = true;
        }

        start() {
            this.count = 0;
            this.renderNextQuestion();
        }

        renderNextQuestion() {
            
            console.log('сработал - renderNextQuestion', this.data[this.count], this.count);

            document.getElementById('game-quest').innerHTML = this.data[this.count].question;
            $('.game-img').attr("src", "/media/" + this.data[this.count].picture);

            document.getElementById('game-answer1').innerHTML = this.data[this.count].answer1;
            document.getElementById('game-answer2').innerHTML = this.data[this.count].answer2;

            if (this.data[this.count].answer2) {
                document.getElementById('game-answer3').innerHTML = this.data[this.count].answer3;
                $('#game-answer3').show();
            }
            else $('#game-answer3').hide();
            if (this.data[this.count].answer4) {
                document.getElementById('game-answer4').innerHTML = this.data[this.count].answer4;
                $('#game-answer4').show();
            }
            else $('#game-answer4').hide();
            if (this.data[this.count].answer5) {
                document.getElementById('game-answer5').innerHTML = this.data[this.count].answer5;
                $('#game-answer5').show();
            }
            else $('#game-answer5').hide();
        }

        checkUserAnswer(userAnswer) {

          console.log('сработал - checkUserAnswer');
          console.log(this.count);

          if (userAnswer === this.trueAnswer) {
            this.result.push(1);
          } else {
            this.result.push(0);
          }

          if (this.count < 9) {
            this.count += 1;
            this.trueAnswer = this.data[this.count].trueAnswer;
            this.renderNextQuestion();
          } else if (this.count === 9) {
            this.end();
          }
        }

        end() {
            let countOfRightAnswers = this.result.reduce((cnt, item) => {
                if (item === 1) { cnt += 1; }
                return cnt;   
            })

            console.log('Конец игры\nRезультат:', this.result);
            console.log('COUNT OF RIGHT ANSWERS = ', countOfRightAnswers);
            
            this.isActive = false;

            requestToServer.command = 'END_GAME';
            webSocketBridge.send(requestToServer);
            
            // рендерить какой нибудь кусок новый станицы с результатом и конгратюлэйшенсом

        }
    }
});
