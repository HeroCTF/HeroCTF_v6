$( document ).ready(async function() {
    if(localStorage.getItem("token")) {
        $("#navbarNavAuth").css("visibility","visible");
    } else {
        $("#navbarNavUnauth").css("visibility","visible");
    }

    if(window.location.hash) {
        hash_content = window.location.hash.split("#")[1];
        data = hash_content.split("=");
        if(data.length === 2) {
            if(data[0] === "popupLogin" && data[1] === "1") {
                $("#msgLogin").append("<p id='msgLoginTxt' style='color: red;'>An error occured, please try to log in again.</p>");
                $("#loginModal").modal('show');
            } else if(data[0] === "popupLogin" && data[1] == "2") {
                $("#msgLogin").append("<p id='msgLoginTxt' style='color: red;'>Please log in before accessing this page.</p>");
                $("#loginModal").modal('show');
            }
        }
        history.replaceState(null, null, ' ');
    }
});

function register() {
    $("#msgRegisterTxt").remove();
    if($("#usernameRegister").val().length == 0 || $("#passwordRegister").val().length == 0 || $("#firstname").val().length == 0 || $("#lastname").val().length == 0) {
        $("#msgRegister").append("<p id='msgRegisterTxt' style='color: red;'>You must fill in all fields.</p>");
        return;
    }
    var data = {"username": $("#usernameRegister").val(), "password": $("#passwordRegister").val(), "firstname": $("#firstname").val(), "lastname": $("#lastname").val()};
    $.ajax({
        url: "/api/register",
        type: "POST",
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        success: function(msg) {
            $("#usernameRegister").val('');
            $("#passwordRegister").val('');
            $("#successRegisterModal").modal('show');
        },
        error: function(msg) {
            let error = msg.responseJSON;
            if(error != undefined) {
                if(msg.status == 400) {
                    $("#msgRegister").append("<p id='msgRegisterTxt' style='color: red;'>"+error["data"]+"</p>");
                } else {
                    $("#msgRegister").append("<p id='msgRegisterTxt' style='color: red;'>Internal Server Error... 😔</p>");
                }
            } else {
                $("#msgRegister").append("<p id='msgRegisterTxt' style='color: red;'>Internal Server Error... 😔</p>");
            }
        }
    })
}

function login() {
    $("#msgLoginTxt").remove();
    if($("#usernameLogin").val().length == 0 || $("#passwordLogin").val().length == 0) {
        $("#msgLogin").append("<p id='msgLoginTxt' style='color: red;'>You must fill in all fields.</p>");
        return;
    }
    var data = {"username": $("#usernameLogin").val(), "password": $("#passwordLogin").val()};
    $.ajax({
        url: "/api/login",
        type: "POST",
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        success: function(msg) {
            localStorage.setItem("token", msg["token"]);
            window.location.href = "/";
        },
        error: function(msg) {
            let error = msg.responseJSON;
            if(error != undefined) {
                if(msg.status == 400) {
                    $("#msgLogin").append("<p id='msgLoginTxt' style='color: red;'>"+error["data"]+"</p>");
                } else {
                    $("#msgLogin").append("<p id='msgLoginTxt' style='color: red;'>Internal Server Error... 😔</p>");
                }
            } else {
                $("#msgLogin").append("<p id='msgLoginTxt' style='color: red;'>Internal Server Error... 😔</p>");
            }
        }
    })
}

$("#loginModal").on('hidden.bs.modal', function() {
    $("#usernameLogin").val("");
    $("#passwordLogin").val("");
    $("#msgLoginTxt").remove();
});

$("#registerModal").on('hidden.bs.modal', function() {
    $("#firstname").val("");
    $("#lastname").val("");
    $("#usernameRegister").val("");
    $("#passwordRegister").val("");
    $("#msgRegisterTxt").remove();
});