window.onload = function () {
    $("#userName").change(function () {
        $.get("/api/alarm/list/alarms", function (data) {
            var alarms = "";
            alarms += "<div id='collapseRegular' class=\"panel-collapse disabled collapse in\" aria-expanded=\"true\">";

            for (var day in data) {
                if (day === 0) {
                    alarms += "<div class=\"panel-body disable\" id=\"regularAlarmSection\">";
                    alarms += "<div class=\"list-group-item-heading\" href=\"#\" disabled=\"\"> " + day + " </div>";
                    alarms += "</div>";
                } else {
                    alarms += "<a class=\"list-group-item\" data-toggle=\"collapse\" href=\"#collapseDay" + day + "\">";
                    alarms += "<div class=\"list-group-item-heading\" href=\"#\"> " + day + " </div>";

                    alarms += "<div id=\"collapseDay" + day + "\" class=\"collapse\">";
                    alarms += "<div class=\"list-group\">";
                    for (var time in day) {
                        alarms += "<a class=\"list-group-item\">";
                        alarms += "<span class=\"mt-1\"> 10:00 </span>";
                        alarms += "<button type=\"button\" class=\"btn btn-danger\" data-toggle=\"modal\" data-target=\"deleteModal(" + alarm + ")\">löschen</button>";
                    }
                    alarms += "</a>";
                    alarms += "</div>";
                    alarms += "</div>";
                    alarms += "</a>"
                }
            }
            alarms += "<div class=\"panel-footer\">";
            alarms += "<button type=\"button\" class=\"btn badge-danger btn-lg\" data-toggle=\"modal\" data-target=\"deleteAllModal('regular')\">alle regulären Wecker löschen</button>";
            alarms += "</div>";
            alarms += "</div>"
            $("#userName").html(alarms);
        });
    });

    $.get("/api/server/list/alarmSounds", function (data) {
        var select = "<label for='alarmSound'>Wähle einen Ton aus, den du als Wecker haben möchtest</label>";
        select += "<select class='form-control' id='alarmSound'>";
        for (var element in data["alarmSounds"]) {
            select += "<option>" + element + "</option>";
        }
        select += "</select>";
        $("#alarmSound").html(select)
    });
}
