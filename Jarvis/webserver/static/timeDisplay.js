function uhr() {
    //Ab hier wird das Datum gebildet
    var jetzt = new Date();
    var tag = jetzt.getDate();
    var monat = jetzt.getMonth() + 1;
    if (monat <= 9)
        monat = '0' + monat;
    var jahr = jetzt.getYear();
    if (jahr < 999)
        jahr += 1900;
    var stunden = jetzt.getHours();
    var minuten = jetzt.getMinutes();

    //Hier werden die Einzelteile zusammengesetzt
    var zeit = tag + '.' + monat + '.' + jahr + ', ' + stunden + ':' + minuten + ' Uhr';

    //Und hier wird das Aussehen festgelegt und alles ins Dokument geschrieben
    document.getElementById('uhr').style.display = 'inline;';    //Art des Elements
    document.getElementById('uhr').innerHTML = zeit;
}