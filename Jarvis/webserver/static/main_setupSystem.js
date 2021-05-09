function finalizeConfig() {
  // freeze all input-boxes and buttons
  $("#mainContentBox input").addClass("disabled").attr("disabled", "disabled");
  $("#mainContentBox button").addClass("disabled").attr("onclick", "");
  $("#button_execute")
    .removeClass("btn-success")
    .addClass("btn-warning")
    .attr("disabled", "disabled")
    .html("aktualisiere…");
  // fetch all data
  data = {
      "voice": $("#speech").val(),
      "homeLocation": $("#homeLocation").val(),
      "messengerKey": $("#telegramSupport").val(),
      "useCameras": $("#useCameras").val() === "Ja",
      "useFaceRec": $("#useFaceRec").val() === "Ja",
      "useInterface": $("#useInterface").val() === "Ja",
  }
  // push data to server
  $.get("/api/writeConfig/system", data, function(data) {
    window.location.replace("/index");
  });
}
