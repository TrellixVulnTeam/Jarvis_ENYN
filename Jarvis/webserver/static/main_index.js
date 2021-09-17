function reloadTime() {
    var time = new Date();
    var timeView = "";
    timeView += "<i class= \"material-icons\">schedule</i> ";
    var hours = (time.getHours() < 10 ? '0' + time.getHours() : time.getHours());
    var minutes = (time.getMinutes() < 10 ? '0' + time.getMinutes() : time.getMinutes());
    timeView += hours + ":" + minutes;
    $("#titleTime").html(timeView);
}

window.onload = function () {
    reloadTime();
    setInterval(reloadTime, 2000);
    $
}