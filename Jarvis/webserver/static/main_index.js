function refreshInformation() {
  $.get("/api/server/status", function(data) {
    if(data["status"] == "running") {
      $("#StartPageServerStatus")
        .removeClass("badge-danger")
        .removeClass("badge-secondary")
        .addClass("badge-success")
        .html("läuft");
      if(data["since"] > 0) {
        duration = Math.floor(Date.now()/1000 - data["since"]);
        if(duration < 60) {
          out = duration + " s";
        } else if (duration < 3600) {
          out = Math.floor(duration/60) + " min";
        } else if (duration < 86400){
          out = Math.floor(duration/3600) + " h";
        } else {
          out = Math.floor(duration/86400) + " d, " + Math.floor((duration-Math.floor(duration/86400))/3600) + " h";
        }
        $("#timestampUptime").html("<span>In Betrieb seit</span><span>" + out + "</span>");
      }
    } else if (data["status"]=="stopped") {
      $("#StartPageServerStatus")
      .removeClass("badge-success")
      .removeClass("badge-secondary")
      .addClass("badge-danger")
      .html("gestoppt");
    } else {
      $("#StartPageServerStatus")
      .removeClass("badge-success")
      .removeClass("badge-danger")
      .addClass("badge-secondary")
      .html("unbekannt");
    }
  });
  $.get("/api/installer/getStatus", function(data) {
    if(data["status"] == "idle") {
      $("#StartPageInstallerStatus")
        .removeClass("badge-success")
        .addClass("badge-danger")
        .html("Nein");
      $("#StartPageInstallerLogs")
        .html("");
    } else {
      $("#StartPageInstallerStatus")
      .removeClass("badge-danger")
      .addClass("badge-success")
      .html("Ja.");
      $("#StartPageInstallerLogs")
      .html("" + data["log"] + "");
    }
  });
  $.get("/api/server/list/*", function(data) {
    var usersBuf = "";
    var ct = 0;
    for (var user in data["users"]) {
      usersBuf += "<span>" + user + " (" + data["users"][user]["first_name"] + " " + data["users"][user]["last_name"] + ")</span><br />";
      ct = ct +1;
    }
    $("#mainUserList").html(usersBuf);
    $("#mainUserListBadge").html("Registrierte Benutzer <span class=\"badge badge-secondary\">" + ct + "</span>");

    var modulesBuf = "";
    var ct = 0;
    for (var module in data["modules"]) {
      modulesBuf += "<span>" + module + "</span><br />";
      if(ct == 3) {
        modulesBuf += '<div class="collapse" id="collapseModuleBox">';
      }
      ct = ct +1;
    }
    if(ct >= 3) {
      modulesBuf += "</div>";
      modulesBuf += "<a href=\"#\" data-toggle=\"collapse\" data-target=\"#collapseModuleBox\" aria-expanded=\"false\">mehr anzeigen…</a>"
    }
    $("#mainModuleList").html(modulesBuf);
    $("#mainModuleListBadge").html("Aktive Module <span class=\"badge badge-secondary\">" + ct + "</span>");

    var externBuf = "";
    var ct = 0;

    for(var extSys in data["externSystems"]){
      externBuf += "<span>" + extSys + "</span><br />";
      if(ct == 3) {
        externBuf += '<div class="collapse" id="collapseSystemBox">';
      }
      ct = ct +1;
    }
    if(ct >= 3) {
      externBuf += "</div>";
      externBuf += "<a href=\"#\" data-toggle=\"collapse\" data-target=\"#collapseSystemBox\" aria-expanded=\"false\">mehr anzeigen…</a>"
    }
    $("#mainExternList").html(externBuf);
    $("#mainExternListBadge").html("Externe Systeme <span class=\"badge badge-secondary\">" + ct + "</span>");

  });
}

function statusServer(action) {
  switch (action) {
    case "start":
      $("#serverStatusStartButton")
        .removeClass("btn-success")
        .addClass("btn-outline-secondary")
        .html("lädt…");
      $.get("/api/server/start", function(data){
        setTimeout(function() {
          $("#serverStatusStartButton")
            .removeClass("btn-outline-secondary")
            .addClass("btn-success")
            .html("System starten");
        }, 200);
      });
      break;
      case "stop":
        $("#serverStatusStopButton")
          .removeClass("btn-danger")
          .addClass("btn-outline-secondary")
          .html("lädt…");
        $.get("/api/server/stop", function(data){
          setTimeout(function() {
            $("#serverStatusStopButton")
              .removeClass("btn-outline-secondary")
              .addClass("btn-danger")
              .html("System stoppen");
          }, 200);
        });
        break;
    default:

  }
}
window.onload = function () {
  refreshInformation();
  setInterval(refreshInformation, 3500);
}
