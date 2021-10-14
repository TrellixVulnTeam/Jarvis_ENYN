function createPHUEBoxes(groups, allLights) {
    let output = "";
    for (var gr in groups) {
        let spezGroup = groups[gr];
        // toDo: disable all lights in group
        output += "<div class=\"card border-primary\">";
        output += "<div class=\"card-header form-inline bg-primary\">";
        output += spezGroup["name"];
        output += "</div>";
        output += "<div className=\"card-body\">";
        output += "<ul class=\"list-group\">";
        let tempLight;
        for (spezLight in spezGroup["lights"]) {
            tempLight = allLights[spezGroup["lights"][spezLight]];
            output += "<li class=\"list-group-item d-flex flex-nowrap justify-content-between\">";
            if (tempLight["on"] === true) {
                output += "<button class=\"btn btn-outline-success\" onclick=\"changePowerstate('" + tempLight["name"] + "', this)\"><i class=\"bi bi-lightbulb-fill\"></i></button>";
            } else {
                output += "<button class=\"btn btn-outline-danger\" onclick=\"changePowerstate('" + tempLight["name"] + "', this)\"><i class=\"bi bi-lightbulb-fill\"></i></button>";
            }
            output += "<span class=\"lampName\"'>" + tempLight["name"] + "</span>";
            output += "<div class='d-flex justify-content-around flex-nowrap'>";
            output += "<span class=\"material-icons-outlined\">brightness_2</span>";
            output += "<input type=\"range\" class=\"form-control-range\" min=\"0\" max=\"254\" value=\"" + tempLight["brightness"] + "\" onchange=\"changeBrightness('" + tempLight["name"] + "', this)\">";
            output += "<span class=\"material-icons-outlined\">light_mode</span></div>";
            output += "</li>";
        }
        output += "</ul>";
        output += "</div></div></div></div>";
    }
    return output;
}

function changeBrightness(lampName, element){
    $.get("/api/phue/change/brightness/"+lampName+"/"+element.value);
}

function changePowerstate(lightname, element) {
    $.get("/api/phue/change/powerState/" + lightname, function () {
        if (element.classList.contains("btn-outline-danger")) {
            element.classList = "btn btn-outline-success";
        } else {
            element.classList = "btn btn-outline-danger";
        }
        refreshInfs();
    });
}

function refreshInfs() {
    var output = "";
    $.get("/api/phue/list/groups", function (groups) {
        $.get("/api/phue/list/lights?id=true", function (allLights) {
            if (groups != null) {
                output += createPHUEBoxes(groups, allLights);
            }
            document.getElementById("lightGroups").innerHTML = output;
        });
    });
}

window.onload = function () {
    refreshInfs();
    setInterval(refreshInfs, 30000);
}
