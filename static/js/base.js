//     *****************************************
//     СКРИПТ ДЛЯ МИНИ ИГРЫ
//     *****************************************
let user_answer = ['0', '0', '0'];
let counter = 0;

let commentsCounter = 0;

function contentMiniGame(data) {
  $('.js-game-not-ready').hide();
  $('.js-game-ready').show();
  $(".tic").removeClass("act");
  document.getElementById('mini-question').textContent = data.pictures[8].question;
  $('#0mini').attr("src", "/media/" + data.pictures[0].url);
  $('#1mini').attr("src", "/media/" + data.pictures[1].url);
  $('#2mini').attr("src", "/media/" + data.pictures[2].url);
  $('#3mini').attr("src", "/media/" + data.pictures[3].url);
  $('#4mini').attr("src", "/media/" + data.pictures[4].url);
  $('#5mini').attr("src", "/media/" + data.pictures[5].url);
  $('#6mini').attr("src", "/media/" + data.pictures[6].url);
  $('#7mini').attr("src", "/media/" + data.pictures[7].url);
  document.getElementById('try-number').textContent = data.number_of_try - 2;
}

function skipGame() {
  $.ajax({

    type: "GET",

    url: "/skip_mini_game/",

    dataType: 'json',

    cache: false,

    success: function (data) {
      if (data.bool) {
        $.ajax({
          type: "GET",

          url: "/next_mini_game/",

          dataType: 'json',

          cache: false,

          success: function (data) {
            checkStageMiniGame();
          }
        });
      }
    }
  });
}

function playerAction(elem, id) {
  if ($(elem).hasClass("act")) {
    $(elem).removeClass("act");
    user_answer[counter] = '0';
    if (counter > 0) {
      counter -= 1;
    }
  } else if (counter < 3) {
    $(elem).addClass("act");
    user_answer[counter] = parseInt(id,10);
    counter += 1;
  }

  if (counter === 3) {
    $.ajax({

      type: "GET",

      url: "/check_answer_for_game/",

      data: { 'user_answer1': user_answer[0],
              'user_answer2': user_answer[1],
              'user_answer3': user_answer[2]},

      dataType: 'json',

      cache: false,

      success: function (data) {
        if (data.bool) {
          $('.js-alert-success').addClass('game__alert_opacity-1');
          $.ajax({

            type: "GET",

            url: "/check_points/",

            dataType: 'json',

            cache: false,

            success: function (data) {
              document.getElementById('bonus').textContent = data.points;
            }
          });
          setTimeout(() => {
             $.ajax({

              type: "GET",

              url: "/next_mini_game/",

              dataType: 'json',

              cache: false,

              success: function (data) {
                $('.js-alert-success').removeClass('game__alert_opacity-1');
                checkStageMiniGame();
              }
            });
           }, 1000)
         
        } else {
          $('.js-alert-error').addClass('game__alert_opacity-1');
          setTimeout(() => {
            $.ajax({

              type: "GET",

              url: "/reload_mini_game/",

              dataType: 'json',

              cache: false,

              success: function (data) {
                $('.js-alert-error').removeClass('game__alert_opacity-1');
                checkStageMiniGame();
              }
            });
          }, 1000)
          
        }
      }
    });
  }
}

$(".tic").click(function(){
  let id = $(this).attr("id");
  let e = document.getElementById(id);
  playerAction(e,id);
});

function miniGameNotReady(time) {
  let constTime;
  $('.js-game-ready').hide();
  $('.js-game-not-ready').show();

  if (time === 'starttimer') {
    constTime = '29:59';
  } else {
    constTime = time.match(/\d*M\d*/g).toString().replace('M', ':');
  }

  function startTimer(timer) {
    if (timer !== undefined) {
      document.getElementById('js-timer').innerText = timer;
    }
    const elem = document.getElementById('js-timer');
    let tim = elem.innerText;
    let min = tim[0] + tim[1];
    let seconds = tim[3] + tim[4];
    if (seconds === '00') {
      if (min === '00') {
        $('.js-game-not-ready').hide();
      }
      min -= 1;
      seconds = '59';
      if (min < '10') min = '0' + min;
    } else {
      seconds -= 1;
    }
    if (seconds < 10) {
      seconds = '0' + seconds;
    }
    elem.textContent = min + ':' + seconds;
    setTimeout(startTimer, 1000);
  }
  startTimer(constTime);
}

function loadMiniGame() {
  $.ajax({

    type: "GET",

    url: "/load_picture/",

    dataType: 'json',

    cache: false,

    success: function (data) {
      if (data.pictures === 0) {
        miniGameNotReady(data.number_of_try);
      } else {
        contentMiniGame(data);
      }
    }
  });
}

function checkStageMiniGame() {
  counter = 0;
  $.ajax({
    type: "GET",
    url: "/check_game_is_ready/",
    cache: false,
    success: function(data){
      if (data.mini_game_is_ready === 1) {
        loadMiniGame();
      } else if (data.timer !== null) {
        miniGameNotReady(data.timer);
      } else {
        miniGameNotReady('starttimer');
      }
    }
  });
}

//     *****************************************




//     *****************************************
//     СКРИПТ ДЛЯ КОММЕНТАРИЕВ
//     *****************************************
function commentsData(objects) {
  for (let i = 0; i < objects.comments.length; i++) {
    document.getElementById("js-user" + i).innerText = objects.comments[i].user;
    $("#js-user" + i).attr("title", objects.comments[i].user);
    document.getElementById("js-text" + i).innerText = objects.comments[i].text;
    const date = objects.comments[i].date.match(/\d*-\d*-\d*/g).toString();
    const newDate = new Date();
    const commentDate = new Date(date);
    if (commentDate.getMonth() === newDate.getUTCMonth() && commentDate.getDate() === newDate.getUTCDate() && commentDate.getFullYear() === newDate.getUTCFullYear()) {
      document.getElementById("js-date" + i).innerText = 'Сегодня';
    } else {
      document.getElementById("js-date" + i).innerText = `${date.slice(8.10)}.${date.slice(5,7)}.${date.slice(0,4)}`;
    }
    
    document.getElementById("js-city" + i).innerText = objects.comments[i].city;
    $("#js-city" + i).attr("title", objects.comments[i].city);
    $('#js-rating' + i).raty({
      score: () => objects.comments[i].rating,
      readOnly: () => true
    });
    const element = document.getElementById('js-avatar' + i);
    $(element).attr("src", objects.comments[i].avatar);
  }
}

function moreCommentsData(comments) {
  const commentHTML = document.querySelector('.comments');
  const templateComment = document.getElementById('templateComment');
  const templateContainer = 'content' in templateComment ? templateComment.content : templateComment;
  const comment = comments;

  for (let i = 0; i < comment.length; i++) {
    const newElementComment = templateContainer.querySelector('.table-comment').cloneNode(true);

    const date = comment[i].date.match(/\d*-\d*-\d*/g).toString();
    const newDate = new Date();
    const commentDate = new Date(date);
    if (commentDate.getMonth() === newDate.getUTCMonth() && commentDate.getDate() === newDate.getUTCDate() && commentDate.getFullYear() === newDate.getUTCFullYear()) {
      newElementComment.querySelector('.js-date').textContent = 'Сегодня';
    } else {
      newElementComment.querySelector('.js-date').textContent = `${date.slice(8.10)}.${date.slice(5,7)}.${date.slice(0,4)}`;
    }

    newElementComment.querySelector('.js-user').textContent = comment[i].user;
    newElementComment.querySelector('.js-user').setAttribute("title", comment[i].user);

    newElementComment.querySelector('.js-city').textContent = comment[i].city;

    const element = newElementComment.querySelector('.js-avatar');
    $(element).attr('src', comment[i].avatar);

    newElementComment.querySelector('.js-text').textContent = comment[i].text;

    commentHTML.appendChild(newElementComment);

    $(newElementComment.querySelector('.js-rating')).raty({
      score: () => comment[i].rating,
      readOnly: () => true
    });
  }
}

function loadComments() {
  $.ajax({
    type: "GET",
    url: "/get_comments/",
    cache: false, 
    success: function(data) {
      commentsData(data);
    }
  });
}


(function() {
     let timer;
     let timer2;

     $('#js-skip-game').click(function() {
      if (timer2) {
        clearTimeout(timer2);
      }

      timer2 = setTimeout(skipGame, 200);
     });

     $('#moreComments').click(function() {
         if (timer) {
             clearTimeout(timer);
         }
         
         timer = setTimeout(loadMoreComments, 200);
     });
}());

const throttle = (func, limit) => {
  let inThrottle = false;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

function loadMoreComments() {
  if (commentsCounter === true || commentsCounter === 3) {
    const comments = document.getElementsByClassName('table-comment');

    for (let i = 3; i < comments.length; i++) {
      $(comments[i]).toggleClass('hide');
    }

    if ($(comments[3]).hasClass('hide')) {
      $('.moreComments').text('Еще отзывы');
    } else {
      $('.moreComments').text('Скрыть отзывы');
    }
    return;
  }

  $.ajax({
    type: 'GET',
    url: '/get_more_comments/',
    cache: false,
    data: {number: commentsCounter},
    success: function(data) {
      moreCommentsData(data.more_comments);

      if (data.bool || commentsCounter === 2) {
        commentsCounter = data.bool;
        $('.moreComments').text('Скрыть отзывы');
        return;
      }

      commentsCounter += 1;
    }
  })
}

function addComment() {
  $("#modalComment").modal();
}

//     *****************************************
function checkPoints() {
$.ajax({

    type: "GET",

    url: "/check_points/",

    cache: false,

    success: function (data) {
      document.getElementById('bonus').textContent = data.points;
    }
});
}

function include(url) {
  var script = document.createElement('script');
  script.src = url;
  document.getElementsByTagName('head')[0].appendChild(script);
}

$.getScript("static/js/jquery.raty.js");
$.getScript("static/js/jquery.sticky.js");

$(document).ready(function() {
  checkPoints();
  loadComments();
  checkStageMiniGame();

  $('#add-comment').click(function () {
    $(this).popover('toggle');
  });  

  $('#stars').raty({
    click: function(score) {
      console.log(score);
    },
    hints: ['Ужасно', 'Плохо', 'Нормально', 'Хорошо', 'Отлично!'],
    target: '#target',
    targetKeep : true,
  });

  $('#panelbody').sticky({topSpacing:0, zIndex:9});

}); 


