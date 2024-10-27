function load_infos(){
    $.ajax({
        cache: false,
        url: "/api/me",
        type: "GET",
        headers: {
            "Authorization": "Bearer "+localStorage.getItem("token")
        },
        success: function(msg){
            $("#firstname").val(msg["firstname"]);
            $("#lastname").val(msg["lastname"]);
            $("#username").val(msg["username"]);
            $("#user_id").val(msg["id"]);
            $("#token").val(localStorage.getItem("token"));
            if(msg["pp"] !== null) {
                $("#pp").attr("src","/api/picture/"+msg["pp"]+"?token="+localStorage.getItem("token"));
                $("#pp").width(200);
                $("#pp").height(200);
            }
        },
        error: function(msg){
            $("#error_content").text("Unexcepted error, please try log in again !")
            $("#unexceptErrorModal").modal('show');
            setTimeout(function(){
                localStorage.removeItem("token");
                window.location.href = "/#popupError=1";
            },3000)
        }
    })
}
    

$( document ).ready(async function() {
    if(!localStorage.getItem("token")) {
        window.location.href = "/#popupLogin=1";
    }
    load_infos();
    $("#picture").on("change", function(){
        document.forms["form_picture"].submit();
    });
});

function save(){
    $("#errorTxt").val('');
    if($("#username").val().length == 0 || $("#firstname").val().length == 0 || $("#lastname").val().length == 0 || $("#user_id").val().length == 0) {
        $("#errorModal").modal('show');
        $("#errorTxt").text("You must fill in all fields.");
        return;
    }
    var data = {"username": $("#username").val(), "firstname": $("#firstname").val(), "lastname": $("#lastname").val(), "id": parseInt($("#user_id").val())};
    $.ajax({
        url: "/api/profile",
        type: "PATCH",
        data: JSON.stringify(data),
        contentType: 'application/json',
        headers:{
            "Authorization": "Bearer "+localStorage.getItem("token")
        },
        dataType: 'json',
        success: function(msg) {
            $("#successModal").modal('show');
            load_infos();
        },
        error: function(msg) {
            let error = msg.responseJSON;
            if(error != undefined) {
                if(msg.status == 400){
                    $("#errorModal").modal('show');
                    $("#errorTxt").text(error["data"]);
                } else if(msg.status == 404) {
                    $("#errorModal").modal('show');
                    $("#errorTxt").text("It seems that your current user does not exist in database, please log in again.");
                    setTimeout(function(){
                        localStorage.removeItem("token");
                        window.location.href = "/#popupError=1";
                    },3000)
                } else if(msg.status == 401) {
                    $("#errorModal").modal('show');
                    $("#errorTxt").text("Nasty things are going on, please log in again.");
                    setTimeout(function(){
                        localStorage.removeItem("token");
                        window.location.href = "/#popupError=1";
                    },3000)
                } else {
                    $("#errorModal").modal('show');
                    $("#errorTxt").text("Internal Server Error... 😔");
                }
            } else {
                $("#errorModal").modal('show');
                $("#errorTxt").text("Internal Server Error... 😔");
            }
        }
    })
}