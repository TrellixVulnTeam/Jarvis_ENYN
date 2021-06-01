function deleteAlarm() {

}

window.onload = function (){
    $("#alarmEnum").change(function () {
        $.get("/api/clock/list/clocks", function (data){
            var regular = "<li class=\"list-group-item\">"

            regular += "</li>"
        })
    })
}