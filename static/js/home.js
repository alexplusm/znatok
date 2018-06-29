var counter_for_theory = 0;

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

$("#modalbtn").click(function () {
  $("#modalLogin").modal();
});