

window.onload = function (){
    $("enumeration").change(function (){
        $.get("/api/phue/list/lights")
    })
}