$(document).ready( function() {
    const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
	const ws_path = ws_scheme + "://" + window.location.host + "/waiting_room/";
	const webSocketBridge = new channels.WebSocketBridge();
    let userId = 0;
    let gameIsEnd = false;
    let result = 0;
    var trueAnswer = '';
    var game = '';
    let group = '';
    let timeStartGame = '';

    let userPoints = 0;
    let userRate = null;


    let requestToServer = {
        command: 'comm',
        user: 'user',
        group: 'group',
        result: 'result',
        timeStartGame: '',
        userRate,
    }

    function retrievePoints() {
        $.ajax({

            type: "GET",

            url: "check_points/",

            cache: false,

            success: function (data) {
                userPoints = data.points;
                renderButtons(userPoints);
            }
        });
    }
    retrievePoints();
    function renderButtons(usPoints) {
        const btn50 = document.getElementById('btn_for_online_2');
        const btn100 = document.getElementById('btn_for_online_3');
        const btn250 = document.getElementById('btn_for_online_4');
        const btn500 = document.getElementById('btn_for_online_5');
        const btn1000 = document.getElementById('btn_for_online_6');

        if (usPoints < 50) {
            btn50.setAttribute('disabled', true);
        }
        if (usPoints < 100) {
            btn100.setAttribute('disabled', true);
        }
        if (usPoints < 250) {
            btn250.setAttribute('disabled', true);
        }
        if (usPoints < 500) {
            btn500.setAttribute('disabled', true);
        }
        if (usPoints < 1000) {
            btn1000.setAttribute('disabled', true);
        }

    }


    const btnForOnlineGame = document.querySelectorAll('.btn_for_online');

    for (var i = 0; i < btnForOnlineGame.length; i++) {
        btnForOnlineGame[i].addEventListener("click", function () {
            userRate = Number(this.innerHTML)
            console.log(userRate);
        }, false);
    }


    const totalEl = document.getElementById('totalCount');
    const winsEl = document.getElementById('countOfWins');
    const statisticEl = document.getElementById('statictic');

    function getStatistic() {
        $.ajax({

            type: "GET",

            url: "get_statistic/",

            cache: false,

            success: function (data) {
                console.log(data);
                totalEl.textContent = data.total;
                winsEl.textContent = data.wins;
                statisticEl.textContent = data.statistic;

            }
        });
    }
    getStatistic();

    // btn_for_online_active


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
            // Start game
                group = data.room
                $("#online-game-place-1").hide();
                $("#online-game-place-2").show();

                timeStartGame = data.timeStartGame;
                requestToServer.timeStartGame = timeStartGame;

                // requestToServer
                game = new Game(data.quests);
                game.start();
        		break;
        	case 3:
            // Юзер получает персональные результаты
                // game.

                console.log(data);
        		break;
        	case 4:
                break;
            case 5:
            // Рендерим обоим юзерам кто победил и их результаты
                console.log(data.winner);
                console.log('%%%%Your ID', userId)
                game.renderResultBlock(userId, data.winner)
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
          $("#online-game-place-wait-results").show();

          console.log('ПОЧЕМУ НЕ РЕНДЕРИТЬСЯФ!!!!')

          document.getElementById("you-result-true").innerHTML = "Правильных ответов: " + countOfRightAnswers;
          document.getElementById("you-result-false").innerHTML = "Не правильных: " + (10 - countOfRightAnswers);
          document.getElementById("you-result-time").innerHTML = "Время: " + resultTime;
        }

        renderResultBlock(userId, winnerId) {
            console.log('РЕНДЕР ResultBlock')
            if (userId === winnerId) {
                document.getElementById("try-or-win").innerHTML = "Победа";
            } else {
                document.getElementById("try-or-win").innerHTML = "Поражение";
            }
            $("#wait-results").hide();
        }

        checkUserAnswer(userAnswer) {

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
          requestToServer.result = countOfRightAnswers;
          requestToServer.user = userId;
          requestToServer.group = group;

          webSocketBridge.send(requestToServer);

          this.renderWaitBlock(timeStartGame, countOfRightAnswers);
        }
    }
});
