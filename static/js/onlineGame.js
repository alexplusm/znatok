$(document).ready( function() {
    const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
	const ws_path = ws_scheme + "://" + window.location.host + "/waiting_room/";
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
        result: 'result',
        timeStartGame: ''
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
                console.log('SUCCESS'); 
        		break;
        	case 2:
                // Start game!
                $("#online-game-place-1").hide();
                $("#online-game-place-2").show();
                requestToServer.timeStartGame = data.timeStartGame;
                game = new Game(data.quests);
                game.start();
        		break;
        	case 3:
            // END GAME => SHOW RESULTS
                console.log(data);
        		break;
        	case 4:
        		break;			
        		
        }

        });
	});

    // обработчик конопок ответов в игре
    $('.game-answbtn').click(function() {
      let userAnswer = $(this).html();
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

        renderThirdBlock(countTrueAnsw) {

          $("#online-game-place-2").hide();
          $("#online-game-place-3").show();
          document.getElementById("you-result-true").innerHTML = "Правильных ответов: " + countTrueAnsw;
          document.getElementById("you-result-false").innerHTML = "Не правильных: " + (10 - countTrueAnsw);
          document.getElementById("you-result-time").innerHTML = "Время: ";
          const text = document.getElementById("try-or-win");
          text.innerHTML = "Поражение";
          $(text).addClass("text-danger");
        }

        renderWaitBlock(resultTime, countOfRightAnswers) {
          $("#online-game-place-2").hide();
          $("#online-game-place-3").show();
          document.getElementById("you-result-true").innerHTML = "Правильных ответов: " + countOfRightAnswers;
          document.getElementById("you-result-false").innerHTML = "Не правильных: " + (10 - countOfRightAnswers);
          document.getElementById("you-result-time").innerHTML = "Время: " + resultTime;
        }

        // renderResultBlock() {


        // }

        checkUserAnswer(userAnswer) {

          console.log('сработал - checkUserAnswer');
          console.log(this.count);

          if (userAnswer === this.trueAnswer) {
            this.result.push(1);
            $(document.getElementById(this.result.length + 'sign')).addClass("circle-done");
          } else {
            this.result.push(0);
            $(document.getElementById(this.result.length + 'sign')).addClass("circle-done");
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
          console.log()
          webSocketBridge.send(requestToServer);

          this.renderThirdBlock(countOfRightAnswers);
        }
    }
});
