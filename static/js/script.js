LunchBox = {};

LunchBox.init = function () {
    LunchBox.bindEvents();
}

LunchBox.bindEvents = function () {
    $("#login").submit(LunchBox.sendLoginRequest);
    $("#offer").submit(LunchBox.sendOfferRequest);
    $(".join").bind("click", LunchBox.joinAMeal);
    // $(window).on("scroll", function() {
    //     var scrollPos = $(window).scrollTop();
    //     if (scrollPos <= 0) {
    //         $('.navbar').removeClass('top-of-page');
    //     } else {
    //         $('.navbar').addClass('top-of-page');
    //     }
    // });
}

LunchBox.sendLoginRequest = function (e) {
    e.preventDefault();
    let user_name = $("#userName").val();
    $.post("/login",
        {
            user_name: user_name
        },
        function (result) {
            if (result["status"] == "ERROR"){
                $("#content-wrap").empty()
                $("#content-wrap").append("<div>Something won't wrong<div/>");
            } else {
                username = result["username"]
                $("#content-wrap").empty()
                $("#content-wrap").append('<div id="content-wrap"><div class="jumbotron"><h1 class="display-4\">Welcome Back Hiilada</h1><p class="lead">Organize a meal for your coworkers or choose one to join</p><hr class="my-4"></div></div>');
            }}, "json");
}



LunchBox.sendOfferRequest = function (e) {
    e.preventDefault();
    let name = $("#name").val();
    let date = $("#date").val();
    let description = $("#description").val();
    let kosher = $("#kosher").is(":checked");
    let vegetarian = $("#vegetarian").is(":checked")
    let vegan = $("#vegan").is(":checked")
    let meat = $("#meat").is(":checked")
    let fish = $("#fish").is(":checked")
    let dairy = $("#dairy").is(":checked")
    let hot = $("#hot").is(":checked")
    let cold = $("#cold").is(":checked")
    let number = $("#number").val()
    // let image = Null
    $.post("/offer",
        {
            name: name,
            date: date,
            description: description,
            kosher: kosher,
            vegetarian: vegetarian,
            vegan: vegan,
            meat: meat,
            fish: fish,
            dairy: dairy,
            hot: hot,
            cold: cold,
            number: number,
            // image: image
        },
        function (result) {
            if (result["status"] == "SUCCESS") {
                $("#content-wrap").empty()
                $("#content-wrap").append("<div>Offer sent successfully<div/>");
            }
            else {
                $("#content-wrap").empty()
                $("#content-wrap").append("<div>Something won't wrong<div/>");
            }
        }, "json");
}

LunchBox.joinAMeal = function(e) {
    mealId = e.target.getAttribute('data-id');
    console.log(mealId);
    $.post(`/dish`, {mealid: mealId},
    function (result) {
        if (result["status"] == "SUCCESS") {
            $("#content-wrap").empty()
            $("#content-wrap").append("<div>Joined successfully<div/>");
        }
        else {
            $("#content-wrap").empty()
            $("#content-wrap").append("<div>Something won't wrong<div/>");
        }
    }, "json");
}

function encodeImageFileAsURL(element) {
    var file = element.files[0];
    var reader = new FileReader();
    reader.onloadend = function() {
        LunchBox.img = reader.result;
        console.log('RESULT', reader.result)
    }
    reader.readAsDataURL(file);
}

$(document).ready(function () {
    LunchBox.init()
});