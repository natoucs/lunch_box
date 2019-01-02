LunchBox = {};

LunchBox.init = function(){
    LunchBox.bindEvents();
    console.log("Inside the init");

}

LunchBox.bindEvents = function(){
    $("#login").submit(LunchBox.sendLoginRequest);
    $("#offer").submit(LunchBox.sendOfferRequest);
}

LunchBox.sendLoginRequest = function(e){
    e.preventDefault();
    let user_name = $("#userName").val();
    $.post("/login",
    {
        user_name: user_name
    },
    function(result){
        console.log(result)
        LunchBox.directToDishes();
    });
    console.log("Inside the prevent");
}

LunchBox.directToDishes = function(){
    $.get("/dishes", function(){
        console.log("Inside the dishes get request");
    })
}

//name, date, description, kosher, vegeterian, 
//vegan, meat, fish, hot, cold, number, image
LunchBox.sendOfferRequest = function(e){
    e.preventDefault();
    let name = $("#name").val();
    let date = $("#date").val();
    let description = $("#description").val();
    let kosher = $("#kosher").val();
    let vegeterian = $("#vegeterian").val();
    let vegan = $("#vegan").val();
    let meat = $("meat").val();
    let fish = $("fish").val();
    let hot = $("hot").val();
    let cold = $("cold").val();
    let image = $("image").val(); 
    $.post("/offer",
    {
        name: name,
        date: date,
        description: description,
        kosher: kosher,
        vegeterian: vegeterian,
        vegan: vegan,
        meat: meat,
        fish: fish,
        hot: hot,
        cold: cold,
        image: image
    },
    function(result){
        console.log(result)
        $("#content-wrap").empty()
        $("#content-wrap").append("<div>Offer sent successfully<div/>");
    });
    console.log("Inside the prevent");
}

$(document).ready(function () {
    LunchBox.init()
    console.log("Inside the ready");
});