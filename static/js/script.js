LunchBox = {};

LunchBox.init = function () {
    LunchBox.bindEvents();
}

LunchBox.bindEvents = function () {
    $("#login").submit(LunchBox.sendLoginRequest);
    $("#offer").submit(LunchBox.sendOfferRequest);
    $("#join").bind(LunchBox.joinAMeal);
}

LunchBox.sendLoginRequest = function (e) {
    e.preventDefault();
    let user_name = $("#userName").val();
    $.post("/login",
        {
            user_name: user_name
        },
        function (result) {
            if (result["status"] == "SUCCESS"){
                window.location.href = '/dishes'
            } else {
                $("#content-wrap").empty()
                $("#content-wrap").append("<div>Something won't wrong<div/>");
            } 
        }, "json");
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
    let hot = $("#hot").is(":checked")
    let cold = $("#cold").is(":checked")
    let number = $("#number").val()
    let image = $("#image").val();
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
            hot: hot,
            cold: cold,
            number: number,
            image: image
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

LunchBox.joinAMeal = function() {
    mealId = $("#meal-id").val();
    $.get(`/dish/${mealId}`,
    function (result) {
        if (result["status"] == "SUCCESS") {
            $("#content-wrap").empty()
            $("#content-wrap").append("<div>Join successfully<div/>");
        }
        else {
            $("#content-wrap").empty()
            $("#content-wrap").append("<div>Something won't wrong<div/>");
        }
    }, "json");
}

$(document).ready(function () {
    LunchBox.init()
});