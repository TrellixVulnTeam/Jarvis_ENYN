
function createPHUEBoxes(groups, allLights){
    let output = "";
    for (var gr in groups) {
        let spezGroup = groups[gr];
        output += "<div class=\"card border-primary\">";
        output += "<div class=\"card-header form-inline bg-primary\">";
        output += spezGroup["name"];
        output += "</div>";
        output += "<div className=\"card-body\">";
        output += "<ul class=\"list-group\">";
        let tempLight;
        for (spezLight in spezGroup["lights"]) {
            tempLight = allLights[spezGroup["lights"][spezLight]];
            output += "<li class=\"list-group-item d-flex justify-content-between align-items-center\">";
            if (tempLight["on"] === true) {
                output += "<button class=\"btn btn-outline-success\" onclick=\"changePowerstate(\""+tempLight["name"]+"\")\"><i class=\"bi bi-lightbulb-fill\"></i></button>";
            } else {
                output += "<button class=\"btn btn-outline-danger\" onclick=\"changePowerstate(\""+tempLight["name"]+"\")\"><i class=\"bi bi-lightbulb-fill\"></i></button>";
            }
            output += "<span style=\"margin-left: 50px\"></span>";
            output += "<span class=\"lampName\">" + tempLight["name"] + "</span>";
            output += "<span style=\"margin-left: 50px\"></span>";
            output += "<span class=\"material-icons-outlined\">brightness_2</span>";
            output += "<input type=\"range\" class=\"form-control-range\" min=\"0\" max=\"254\" value=\"" + tempLight["brightness"] + "\">";
            output += "<span class=\"material-icons-outlined\">light_mode</span>";
            output += "</li>";

        }
        output += "</ul>";
        output += "</div></div></div></div>";
    }

    return output;
}

function changePowerstate(lightname){
    $.get("/api/phue/change/powerState/"+lightname, function (){
        console.log("lamp updated.");
    });
}

window.onload = function (){
    var output = "";
    $.get("/api/phue/list/groups", function (groups){
        $.get("/api/phue/list/lights?id=true", function (allLights){
            if (groups != null){
                output += createPHUEBoxes(groups, allLights);
            }
            document.getElementById("lightGroups").innerHTML = output;
        });
    });
}

