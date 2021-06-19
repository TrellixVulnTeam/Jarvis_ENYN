function deleteAlarm(alarm, regular, day) {
    // /api/alarm/<action>/<regular>/<day>/<time>
    if (regular){
        $("#modalTime").html("Möchtest du den regulären Wecker um " + alarm + " an jedem " + day + " wirklich löschen?")
    }else{
        $("#modalTime").html("Möchtest du den Wecker um " + alarm + " am " + day + " wirklich löschen?")
    }

    $.get("/api/alarm/delete/"+regular+day+alarm["Zeit"])
}

window.onload = function (){

}
