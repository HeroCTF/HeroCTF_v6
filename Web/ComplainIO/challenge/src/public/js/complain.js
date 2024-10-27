let uuid;

function load_infos(){
    $.ajax({
        url: "/api/complains",
        type: "GET",
        headers: {
            "Authorization": "Bearer "+localStorage.getItem("token")
        },
        success: function(msg){
            let html = "";
            for(var i=0; i<msg.length; i++) {
                html += '<div class="col-md-4 mb-4"><div class="card h-100"><div class="card-body"><h5 class="card-title">Complain template n°'+msg[i]["id"]+'</h5><p class="card-text">'+msg[i]["reason"]+'</p><a href="#" class="btn btn-primary" onclick="template(\''+msg[i]["file_id"]+'\')">Create template</a></div></div></div>'
            }
            $("#complains").append(html);
        },
        error: function(msg){
            $("#error_content").text("Unexcepted error, please try log in again !");
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
});

function template(uuid) {
    $.ajax({
        url: "/api/me",
        type: "GET",
        headers: {
            "Authorization": "Bearer "+localStorage.getItem("token")
        },
        success: function(msg){
            $("#firstname").val(msg["firstname"]);
            $("#lastname").val(msg["lastname"]);
            $("#user_id").val(msg["id"]);
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
    $("#uuid").val(uuid);
    $("#token").val(localStorage.getItem("token"));
    $("#changeModal").modal('show');
}

function create_template(){
    $("#changeModal").modal("hide");
    $("#msgTemplateTxt").remove()
    if($("#firstname").val().length == 0 || $("#lastname").val().length == 0) {
        $("#msgTemplate").append("<p id='msgTemplateTxt' style='color: red;'>You must fill in all fields.</p>");
        return;
    }
    var data = {"firstname": $("#firstname").val(), "lastname": $("#lastname").val(), "uuid": $("#uuid").val(), "id": parseInt($("#user_id").val())}
    $.ajax({
        url: "/api/create_template",
        type: "POST",
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        headers: {
            "Authorization": "Bearer "+localStorage.getItem("token")
        },
        success: function(msg){
            var a = document.createElement("a");
            a.href= "data:application/octet-stream;base64,"+msg["data"];
            a.download = "complain.odt";
            a.click();
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
    $("#firstname").val("");
    $("#lastname").val("");
}

$("#changeModal").on('hidden.bs.modal', function() {
    $("#firstname").val("");
    $("#lastname").val("");
});