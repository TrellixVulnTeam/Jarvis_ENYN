function deleteAlarm(alarm, regular, day) {
    // /api/alarm/<action>/<regular>/<day>/<time>
    $("#deleteModalConfirmButton").addClass("disabled");
    $.get("/api/alarm/delete/"+regular+day+alarm["Zeit"]);
}

function deleteAllAlarms(regular) {}

function getAlarm(regular, alarm_list) {
    var alarms = "";
    alarms += "<div id='collapseRegular' class=\"panel-collapse disabled collapse in\" aria-expanded=\"true\">";
    for (var day in alarm_list){
        if (day === 0){
            alarms += "<div class=\"panel-body disable\" id=\"regularAlarmSection\">";
            alarms += "<div class=\"list-group-item-heading\" href=\"#\" disabled=\"\"> " + day + " </div>";
            alarms += "</div>";
        } else {
            alarms += "<a class=\"list-group-item\" data-toggle=\"collapse\" href=\"#collapseDay" + day + "\">";
            alarms += "<div class=\"list-group-item-heading\" href=\"#\"> " + day + " </div>";
            alarms += "<div id=\"collapseDay"+ day +"\" class=\"collapse\">";
            alarms += "<div class=\"list-group\">";
            for (var time in day){
                alarms += "<a class=\"list-group-item\">";
                alarms += "<span class=\"mt-1\"> 10:00 </span>";
                alarms += "<button type=\"button\" class=\"btn btn-danger\" data-toggle=\"modal\" data-target=\"deleteModal("+alarm+")\">löschen</button>";
            }
            alarms += "</a>";
            alarms += "</div>";
            alarms += "</div>";
            alarms += "</a>";
        }
    }
    alarms += "<div class=\"panel-footer\">";
    alarms += "<button type=\"button\" class=\"btn badge-danger btn-lg\" data-toggle=\"modal\" data-target=\"deleteAllModal('regular')\">alle regulären Wecker löschen</button>";
    alarms += "</div>";
    alarms += "</div>"
    $("#regularAlarmSection").html(alarms);
}

$("#deleteModal").onload = function (alarm, regular, day){
    if (regular){
        $("#deleteModalTime").html("Möchtest du den regulären Wecker um " + alarm + " an jedem " + day + " wirklich löschen?");
    }else{
        $("#deleteModalTime").html("Möchtest du den Wecker um " + alarm + " am " + day + " wirklich löschen?");
    }
    $("#deleteModalConfirmButton").onclick("deleteAlarm(alarm, regular, day)");
}

window.onload = function (){
    $.get("/api/alarm/list/alarms",
        function (data){
        var alarms = "";
        isPresent = data["regularPresent"];
        data = data["regular_alarm"];
        alarms += "<div id='collapseRegular' class=\"panel-collapse disabled collapse in\" aria-expanded=\"true\">";
        if(isPresent){
            for (var day in data){
                if (data[day].length == 0){
                    alarms += "<div class=\"panel-body disable\" id=\"regularAlarmSection\">";
                    alarms += "<div class=\"list-group-item-heading\" href=\"#\" disabled=\"\"> " + day + "</div>";
                    alarms += "</div>";
                } else {
                    alarms += "<a class=\"list-group-item\" data-toggle=\"collapse\" href=\"#collapseDay" + day + "\">";
                    alarms += "<div class=\"list-group-item-heading\" href=\"#\"> " + day + " " + "<span class=\"badge pull-right badge-secondary\">" + data[day].length + "</span> </div>";
                    alarms += "<div id=\"collapseDay"+ day +"\" class=\"collapse\">";
                    alarms += "<div class=\"list-group\">";
                    for (var time in data[day]){
                        alarms += "<a class=\"list-group-item\">";
                        alarms += "<span class=\"mt-1\">" + data[day][time]["time"]["time_stamp"] + "</span>";
                        alarms += "<button type=\"button\" class=\"btn pull-right btn-danger btn-sm\" data-toggle=\"modal\" data-target=\"deleteModal("+time+")\">löschen</button>";
                    }
                    alarms += "</a>";
                    alarms += "</div>";
                    alarms += "</div>";
                    alarms += "</a>";
                }
            }
        }else{
            alarms += "<div class=\"panel-body disable\">"
            alarms += "<div class=\"alert alert-info\">";
            alarms += "<strong>Info!</strong> Keine regulären Wecker eingerichtet.";
            alarms += "</div></div>";
        }

        alarms += "<div class=\"panel-footer\">";
        if(isPresent){
            alarms += "<button type=\"button\" class=\"btn pull-right badge-danger btn-sm\" data-toggle=\"modal\" data-target=\"deleteAllModal('regular')\">alle regulären Wecker löschen</button>";
        }
        alarms += "</div>";
        alarms += "</div>";
        $("#regularAlarmSection").html(alarms);
    }
    );
}
