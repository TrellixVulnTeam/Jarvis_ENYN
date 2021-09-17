var editModalTitle = document.getElementById("editModalTitle");
var editModalHours = document.getElementById("editModalHours");
var editModalMinute = document.getElementById("editModalMinutes");
var editModalText = document.getElementById("editModalText");
var editModalSound = document.getElementById("alarmSoundAudio");
var playSoundButton = document.getElementById("editModalPlaySound");

var deleteModalRepeat = document.getElementById("deleteModalRepeat");
var deleteModalDay = document.getElementById("deleteModalDay");
var deleteModalTime = document.getElementById("deleteModalTime");

var deleteConfirmToast = $("#deleteConfirmToast");

var audio = null;


function editAlarmModal(regular, day, hour, minute, time_stamp, text, sound) {
    let reg = "";
    if (regular) {
        reg = "jeden ";
    }

    editModalTitle.innerHTML = reg + day + ": " + time_stamp;
    editModalHours.value = hour;
    editModalMinute.value = minute;
    editModalText.value = text;
    editModalSound.value = sound;
    $('#editModal').modal('toggle');
}

function deleteAlarmModal(regular, day, hour, minute, time_stamp) {
    let reg = "";

    if (regular) {
        reg = " jeden ";
    }
    deleteModalRepeat.innerHTML = reg;
    deleteModalDay.innerHTML = reg + day;
    deleteModalTime.innerHTML = time_stamp;
    document.getElementById("deleteModalDelButton").onclick = function () {
        deleteAlarm(regular, day, hour, minute, time_stamp)
    };
    document.getElementById("deleteModalDelButton").addEventListener("click", function () {
        console.log("clicked");
        deleteAlarm(regular, day, hour, minute, time_stamp)
    });
    $('#deleteModal').modal('toggle');
}

function saveAlarmChanges(element) {

}

function deleteAlarm(repeat, day, hour, minute) {
    try {
        $.get("api/alarm/delete/" + repeat + "/" + day + "/" + hour + "/" + minute);
        createAlarmList();
        $('#deleteModal').modal('hide');
        document.getElementById("confirmToastHeader").innerHTML = "Wecker wurde erfolgreich gelöscht";
        if (repeat == "regular") {
            document.getElementById("deleteConfirmToastRepeat").innerHTML = "regelmäßiger ";
        } else {
            document.getElementById("deleteConfirmToastRepeat").innerHTML = "";
        }
        document.getElementById("deleteConfirmToastTime").innerHTML = "<b>" + hour + ":" + minute + "Uhr</b>";
        document.getElementById("deleteConfirmToastMessageExtension").innerHTML = " wurde <b>erfolgreich</b> gelöscht!";
        showToastAndClose();
    } catch (e) {
        console.log(e);
        document.getElementById("confirmToastHeader").innerHTML = "Wecker konnte nicht gelöscht werden!";
        if (repeat == "regular") {
            document.getElementById("deleteConfirmToastRepeat").innerHTML = "regelmäßiger ";
        } else {
            document.getElementById("deleteConfirmToastRepeat").innerHTML = " konnte <b>nicht</b> gelöscht werden! Bitte versuche es erneut.";
        }
        document.getElementById("deleteConfirmToastTime").innerHTML = "<br>" + hour + ":" + minute + "Uhr</b>";
        showToastAndClose();
    }
}

function showToastAndClose() {
    deleteConfirmToast.toast('show');
}

function deleteAllAlarms() {

}

function changeAlarmActivity(repeat, day, hour, minute) {

}

function playStopAlarmSound(event) {
    if (event == "click") {
        let button = document.getElementById("editModalPlaySound");
        if (button.lastChild.innerHTML == "play_arrow") {
            audio = new Audio("/api/getAlarmSound/" + editModalSound.innerHTML);
            audio.play();
            button.lastChild.innerHTML = "stop";
        } else {
            audio.pause();
        }
    }
}

function createAlarmList() {
    $.get("/api/alarm/list/alarms", function (data) {
        let alarm_list = "";
        let regularCardBody = document.getElementById("regularCardBody");
        if (data["regularPresent"]) {
            alarm_list += "<ul class=\"list-group\">";

            for (let day in data["regular_alarm"]) {
                if (data["regular_alarm"][day].length == 0) {
                    alarm_list += "<a class=\"list-group-item disabled\">" + day + "</a>";
                } else {
                    alarm_list += "<a class=\"list-group-item list-group-item-action list-group-item-info d-flex justify-content-between align-items-center\" href=\"#collapse" + day + "Regular\" data-toggle=\"collapse\">";
                    alarm_list += day + "<span class=\"badge badge-info badge-pill\">" + data["regular_alarm"][day].length + "</span></a>";
                    alarm_list += "<ul class=\"collapse\" id=\"collapse" + day + "Regular\">";
                    for (let alarm in data["regular_alarm"][day]) {
                        alarm_list += "<li class=\"list-group-item d-flex justify-content-between align-items-center\">";
                        alarm_list += "<div>" + data["regular_alarm"][day][alarm]["time"]["time_stamp"];
                        alarm_list += "<div><button class=\"btn btn-primary\" onclick=\"editAlarmModal('regular','" + day + "','" + data["regular_alarm"][day][alarm]["time"]["hour"] + "','" + data["regular_alarm"][day][alarm]["time"]["minute"] + "','" + data["regular_alarm"][day][alarm]["time"]["time_stamp"] + "','" + data["regular_alarm"][day][alarm]["text"] + "','" + data["regular_alarm"][day][alarm]["sound"] + "')\"><span class=\"material-icons-outlined\" style=\"font-size: 1.2em;\">edit</span></button>";
                        alarm_list += "<button class=\"btn btn-danger\" onclick=\"deleteAlarmModal('regular','" + day + "','" + data["regular_alarm"][day][alarm]["time"]["hour"] + "','" + data["regular_alarm"][day][alarm]["time"]["minute"] + "','" + data["regular_alarm"][day][alarm]["time"]["time_stamp"] + "')\"><span class=\"material-icons-outlined\" style=\"font-size: 1.2em;\">delete</span></button>";
                        alarm_list += "</div></li>";
                    }
                    alarm_list += "</ul>";
                }
            }


        } else {
            alarm_list += "<div class=\"alert alert-info\"><strong>Info!</strong> Keine regulären Wecker eingerichtet.</div>";
        }
        alarm_list += "</div></div>";

        regularCardBody.innerHTML = alarm_list;
    });
}

function showCreateAlarmModal(repeat) {

}

window.onload = function () {
    $.get("/api/alarm/list/alarmSounds", function (data) {
        let soundHTML = "";
        for (sound in data["alarmSounds"]) {
            soundHTML += "<option>" + data["alarmSounds"][sound] + "</option>"
        }
        document.getElementById("editModalSounds").innerHTML = soundHTML;
    });
    createAlarmList();
}

//<input type="checkbox" class="custom-control-input" id="customSwitch1">