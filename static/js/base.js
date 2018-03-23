//     *****************************************
//     СКРИПТ ДЛЯ МИНИ ИГРЫ
//     *****************************************
let user_answer = ['0', '0', '0'];
let counter = 0;

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
          $('.js-alert-success').show();
          $.ajax({

            type: "GET",

            url: "/check_points/",

            dataType: 'json',

            cache: false,

            success: function (data) {
              document.getElementById('bonus').textContent = data.points;
              document.getElementById('bonus1').textContent = data.points;
            }
          });

          $.ajax({

            type: "GET",

            url: "/next_mini_game/",

            dataType: 'json',

            cache: false,

            success: function (data) {
              checkStageMiniGame();
            }
          });
        } else {
          $('.js-alert-error').show();
          $.ajax({

            type: "GET",

            url: "/reload_mini_game/",

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
      contentMiniGame(data);
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
      document.getElementById("js-text" + i).innerText = objects.comments[i].text;
      document.getElementById("js-date" + i).innerText = objects.comments[i].date.match(/\d*-\d*-\d*/g);
      document.getElementById("js-city" + i).innerText = objects.comments[i].city;
      document.getElementById("js-rating" + i).innerText = objects.comments[i].rating;
      const element = document.getElementById('js-avatar' + i);
      $(element).attr("src", objects.comments[i].avatar);
    }
  }
  
  function loadComments() {
    $.ajax({
      type: "GET",
      url: "/get_comments/",
      cache: false,
      success: function(data){
        commentsData(data);
      }
    });
  }
//     *****************************************
  $(document).ready(function() {
    loadComments();
    checkStageMiniGame();
  });
  
  var counter_for_theory = 0;
  jQuery(document).ready(function($) {
var
  $window = $(window),
  $target = $("#panelbody"),
  $h = $target.offset().top;
$window.on('scroll', function() {
  var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  if (scrollTop > $h) {
    $("#panelbody1").addClass("show_block");
  } else {
    $("#panelbody1").removeClass("show_block");
  }
});
});
$(".navitem").click(function(){
  var id = $(this).attr("id");
  var e = document.getElementById(id);
  $(".navitem").removeClass("active");
  $(e).addClass("active");
});

$(".navitem1").click(function(){
  var id = $(this).attr("id");
  var e = document.getElementById(id);
  $(".navitem1").removeClass("active");
  $(e).addClass("active");

  if ((id === "block1") && (counter_for_theory === 0)) {
    counter_for_theory++;
    $(".btnquest").addClass("hide");
    $(".top5").addClass("hide");
    $(".top6").removeClass("hide");
    $(".b1").addClass("hide");
    $(".b2").removeClass("hide");
  } else if((id === "block1") && (counter_for_theory === 1)) {
    $(".btnquest").removeClass("hide");
    $(".top5").removeClass("hide");
    $(".top6").addClass("hide");
    $(".b1").removeClass("hide");
    $(".b2").addClass("hide");
    counter_for_theory = 0;
    $("#block2").addClass("active");
    $("#block1").removeClass("active");
  }

  if (id === "block1_team") {
    $(".img_team").addClass("hide");
    $("#activity").removeClass("hide");
  } else if (id === "block2_team") {
    $(".img_team").addClass("hide");
    $("#volunteers").removeClass("hide");
  } else if (id === "block3_team") {
    $(".img_team").addClass("hide");
    $("#business").removeClass("hide");
  } else if (id === "block4_team") {
    $(".img_team").addClass("hide");
    $("#investors").removeClass("hide");
  } else if (id === "block5_team") {
    $(".img_team").addClass("hide");
    $("#developers").removeClass("hide");
  } else if (id === "block6_team") {
    $(".img_team").addClass("hide");
    $("#agencies").removeClass("hide");
  }
});

$(document).ready(function(){
  $.ajax({

      type: "GET",

      url: "/check_points/",

      cache: false,

      success: function (data) {
        document.getElementById('bonus').textContent = data.points;
        document.getElementById('bonus1').textContent = data.points;
      }
  });

  $("#cat1").addClass("active");
  $("#block2").addClass("active");

  var l1 = document.getElementById("lamb1");
  var l2 = document.getElementById("lamb2");
  var l3 = document.getElementById("lamb3");
  var select = 0;
  
  $(".confirm").addClass("disabled");

  $(".lamb").click(function(){
    var id = $(this).attr("id");
    var e = document.getElementById(id);
    userAction(e, id, l1, l2, l3);
});

  function userAction(elem, id, l1, l2, l3) {
    if ($(elem).hasClass("lambact")) {
      $(elem).removeClass("lambact");
      select = 0;
      $(".confirm").addClass("disabled");
    } else {
      if ((elem != l1) && (elem != l2)) {
        $(elem).addClass("lambact");
        $(l1).removeClass("lambact");
        $(l2).removeClass("lambact");
        $(".confirm").removeClass("disabled");
        select = 3;
      } else if ((elem != l1) && (elem != l3)) {
        $(elem).addClass("lambact");
        $(l1).removeClass("lambact");
        $(l3).removeClass("lambact");
        $(".confirm").removeClass("disabled");
        select = 2;
      } else if ((elem != l2) && (elem != l3)) {
        $(elem).addClass("lambact");
        $(l2).removeClass("lambact");
        $(l3).removeClass("lambact");
        $(".confirm").removeClass("disabled");
        select = 1;
      } else {
        select = 0;
      }
    }

    $(".confirm").click(function(){
      confirmSelection(select);
  });
  }

  function confirmSelection(select) {

  }
});


$(document).ready(function() {
    $("#modalbtn").click(function () {
        $("#modalLogin").modal();
    });
});
