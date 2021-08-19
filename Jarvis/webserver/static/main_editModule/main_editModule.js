function finalizeEdit(moduleName) {
    // freeze all input-boxes and buttons
    editor.setReadOnly(true);
    $("#codeBox input").addClass("disabled").attr("disabled", "disabled");
    $("#codeBox button").addClass("disabled").attr("onclick", "");
    $("#buttonSave")
        .addClass("disabled")
        .attr("disabled", "disabled")
        .html("aktualisiere…");

    // fetch all data
    newCode = editor.getValue();

    // push data to server
    $.get("/api/module/" + moduleName, newCode, function (data) {
    });
}

function saveAndRedirect(oldModuleName, moduleName){
    finalizeEdit(oldModuleName);
    window.location.replace(moduleName);
}

function redirectToSite(moduleName){
    // just  modal if code changed!!!!!!!!!!!!!!!!!!!!!!!!!
    $("#saveModalBody").html("Soll der neue Stand von dem Modul {{ moduleName }} gespeichert werden? Anschließend würde es neu geladen werden.");
    var saveModalFooter = "<div class=\"btn-group\">";
    saveModalFooter += "<button type=\"button\" class=\"btn badge-success\" onclick='saveAndRedirect({{ moduleName }})' ' id=\"buttonSave\" onclick=\"finalizeEdit( \"{{ moduleName }}\" )\"> speichern </button>";
    saveModalFooter += "<button type=\"button\" class=\"btn badge-danger\" onclick='window.location.replace(\"/editModules/\"+moduleName);' id=\"buttonDiscard\"> nicht speichern </button>"
    $("#saveModalFooter").html(saveModalFooter);
    $("#saveModal").trigger('focus');
}

window.onload = function () {
    $.get("/api/server/list/modules", function (data) {
        console.log(data);
        var moduleList = "";
        moduleList += "<div class=\"btn-group-vertical\">";
        for (var module in data) {
            moduleList += "<button type=\"button\" class=\"btn btn-primary\" onclick='redirectToSite(\"" + module + "\") data-toggle=\"modal\" data-target=\"#saveModal\"'>" + module + "</button>"
        }
        moduleList += "</div>";
        $("#moduleList").html(moduleList)
    });

    var editor = ace.edit("editor");
    // editor.setTheme($.get("/static/codeEditDarkTheme.js"));
    editor.setAutoScrollEditorIntoView(true);
    editor.session.setMode($.get("/static/codeEditPythonMode.js"));
}

