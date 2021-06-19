function deleteAlarm(alarm, regular, day) {
    // /api/alarm/<action>/<regular>/<day>/<time>

    $.get("/api/alarm/delete/"+regular+day+alarm["Zeit"])
}

window.onload = function (){
    $("#alarmEnum").change(function () {
        $.get("/api/alarm/list/alarms", function (data){

        });
    });

}