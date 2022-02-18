function refreshWeather(icon){
    icon = parseInt(icon);
    let time = "";
    let weatherIcon = "moon-new.svg";
    let weatherKind = "";
    if (date.getHours() >= 22 || date.getHours() <= 6){
       time = "-night";
    }else {
        time = "-day";
    }
    if (icon >= 200 && icon <= 202){
        weatherIcon = "thunderstorms"+time+"-rain.svg";
        weatherKind = "thunder";
    } else if (icon >= 210 && icon <= 212){
        weatherIcon = "thunderstorms"+time+"-rain.svg";
        weatherKind = "thunder";
    } else if (icon == 221){
        weatherIcon = "lightning-bolt.svg";
        weatherKind = "thunder";
    } else if (icon >= 230 && icon <= 232){
        weatherIcon = "thunderstorms"+time+"-rain.svg";
        weatherKind = "thunder";
    } else if (icon == 300){
        weatherIcon = "partly-cloudy"+time+"-drizzle.svg";
        weatherKind = "cloudy";
    } else if (icon == 301 || icon == 302){
        weatherIcon = "partly-cloudy"+time+"-drizzle.svg";
        weatherKind = "rainy"
    } else if (icon >= 310 && icon <= 314){
        weatherIcon = "partly-cloudy"+time+"-drizzle.svg";
        weatherKind = "rainy";
    } else if (icon == 321){
        weatherIcon = "partly-cloudy"+time+"-rain.svg";
        weatherKind = "rainy";
    } else if (icon == 500){
        weatherIcon = "partly-cloudy"+time+"-drizzle.svg";
        weatherKind = "rainy";
    }else if (icon >= 501 && icon <= 502){
        weatherIcon = "partly-cloudy"+time+"-rain.svg";
        weatherKind = "rainy";
    }else if (icon >= 503 && icon <= 504){
        weatherIcon = "rain.svg";
        weatherKind = "rainy";
    } else if (icon == 511){
        weatherIcon = "partly-cloudy"+time+"-sleet.svg";
        weatherKind = "rainy";
    } else if (icon >= 520 && icon <= 531){
        weatherIcon = "rain.svg";
        weatherKind = "rainy";
    } else if (icon >= 600 && icon <= 602){
        weatherIcon = "partly-cloudy"+time+"-snow.svg";
        weatherKind = "snowy";
    } else if (icon >= 611 && icon <= 616){
        weatherIcon = "partly-cloudy"+time+"-sleet.svg";
        weatherKind = "rainy";
    } else if (icon == 620 || icon == 621){
        weatherIcon = "partly-cloudy"+time+"-snow.svg";
        weatherKind = "snowy";
    } else if (icon == 622){
        weatherIcon = "snow.svg";
        weatherKind = "snowy";
    } else if (icon == 701){
        weatherIcon = "mist.svg";
        weatherKind = "misty";
    } else if (icon == 711){
        weatherIcon = "partly-cloudy"+time+"smoke.svg";
        weatherKind = "stormy";
    } else if (icon == 721){
        weatherIcon = "haze"+time+".svg";
        weatherKind = "stormy";
    } else if (icon == 731){
        weatherIcon = "dust"+time+".svg";
        weatherKind = "stormy";
    } else if (icon == 741){
        weatherIcon = "fog"+time+".svg";
        weatherKind = "misty";
    } else if (icon == 751){
        weatherIcon = "dust-wind.svg";
        weatherKind = "stormy";
    } else if (icon == 761){
        weatherIcon = "dust"+time+".svg";
        weatherKind = "stormy";
    } else if (icon == 762){
        weatherIcon = "smoke.svg";
        weatherIcon = "vulcan";
    } else if (icon == 771){
        weatherIcon = "haze"+time+".svg";
        weatherKind = "stormy";
    } else if (icon == 781){
        weatherIcon = "tornado.svg";
        weatherKind = "stormy";
    } else if (icon == 800){
        weatherIcon = "clear"+time+".svg";
        weatherKind = "sunny";
    } else if (icon == 801 ||icon == 802){
        weatherIcon = "partly-cloudy"+time+".svg";
        weatherKind = "partly_cloudy";
    } else if (icon == 803){
        weatherIcon = "cloudy.svg";
        weatherKind = "cloudy";
    } else if (icon == 804){
        weatherIcon = "overcast.svg";
        weatherKind = "cloudy";
    }else{
        console.log("Unknkown Icon!");
    }
    return [weatherIcon, weatherKind];
}

function refreshBackgroundAndText(weatherKind){
    var cards = document.getElementsByClassName("day-card");
    if (weatherKind == "thunder"){
        if (old_bg != "background_thunder.jpg"){
            document.body.style.backgroundImage = "url('static/img/weatherBackground/background_thunder.jpg')";
            document.body.style.color = "white";
            for (var i = 0; i < cards.length; i++){
                cards[i].style.color = "white";
            }
            changeTempCharXYColor("white");
            old_bg = "background_thunder.jpg";

            document.getElementById("buttonTempChart").classList.replace("btn-outline-dark", "btn-dark");
            document.getElementById("buttonPercChart").classList.replace("btn-outline-dark", "btn-dark");
            document.getElementById("buttonHumiChart").classList.replace("btn-outline-dark", "btn-dark");
        }
    }
    else if (date.getHours() >= 22 || date.getHours() <= 6 || weatherKind == "night"){
        if (old_bg != "background_night.jpg"){
            document.body.style.backgroundImage = "url('static/img/weatherBackground/background_night.jpg')";
            document.body.style.color = "white";
            for (var i = 0; i < cards.length; i++){
                cards[i].style.color = "white";
            }
            changeTempCharXYColor("white");
            document.getElementById("buttonTempChart").classList.replace("btn-outline-dark", "btn-dark");
            document.getElementById("buttonPercChart").classList.replace("btn-outline-dark", "btn-dark");
            document.getElementById("buttonHumiChart").classList.replace("btn-outline-dark", "btn-dark");
        }
    }else if (weatherKind == "misty"){
        if (old_bg != "background_misty.jpg"){
            document.body.style.backgroundImage = "url('static/img/weatherBackground/background_misty.jpg')";
            document.body.style.color = "black";
            for (var i = 0; i < cards.length; i++){
                cards[i].style.color = "black";
            }
            changeTempCharXYColor("black");
            document.getElementById("buttonTempChart").classList.replace("btn-dark", "btn-outline-dark");
            document.getElementById("buttonPercChart").classList.replace("btn-dark", "btn-outline-dark");
            document.getElementById("buttonHumiChart").classList.replace("btn-dark", "btn-outline-dark");
        }
    }else if (weatherKind == "sunny"){
        if (old_bg != "background_sunny.jpg"){
            document.body.style.backgroundImage = "url('static/img/weatherBackground/background_sunny.jpg')";
            document.body.style.color = "black";
            for (var i = 0; i < cards.length; i++){
                cards[i].style.color = "black";
            }
            changeTempCharXYColor("black");
            document.getElementById("buttonTempChart").classList.replace("btn-dark", "btn-outline-dark");
            document.getElementById("buttonPercChart").classList.replace("btn-dark", "btn-outline-dark");
            document.getElementById("buttonHumiChart").classList.replace("btn-dark", "btn-outline-dark");
        }
    } else if (weatherKind.includes("cloudy")){7
        if (weatherKind.includes("partly")){
            if (old_bg != "background_partly_cloudy.jpg"){
                document.body.style.backgroundImage = "url('static/img/weatherBackground/background_partly_cloudy.jpg')";
                old_bg = "background_partly_cloudy.jpg";
            }
        }else if (old_bg != "background_cloudy.jpg"){
            document.body.style.backgroundImage = "url('static/img/weatherBackground/background_cloudy.jpg')";
            old_bg = "background_cloudy.jpg";
        }
        document.body.style.color = "black";
        for (var i = 0; i < cards.length; i++){
            cards[i].style.color = "black";
        }
        document.getElementById("buttonTempChart").classList.replace("btn-dark", "btn-outline-dark");
        document.getElementById("buttonPercChart").classList.replace("btn-dark", "btn-outline-dark");
        document.getElementById("buttonHumiChart").classList.replace("btn-dark", "btn-outline-dark");
        changeTempCharXYColor("black");

    } else if (weatherKind == "rainy"){
        if (old_bg != "background_rainy.jpg"){
            document.body.style.backgroundImage = "url('static/img/weatherBackground/background_rainy.jpg')";
            document.body.style.color = "white";
            for (var i = 0; i < cards.length; i++){
                cards[i].style.color = "white";
            }
            old_bg = "background_rainy.jpg";
            changeTempCharXYColor("white");
            document.getElementById("buttonTempChart").classList.replace("btn-outline-dark", "btn-dark");
            document.getElementById("buttonPercChart").classList.replace("btn-outline-dark", "btn-dark");
            document.getElementById("buttonHumiChart").classList.replace("btn-outline-dark", "btn-dark");
        }

    } else if (weatherKind == "snowy" && old_bg != "background_snow.jpg"){
        document.body.style.backgroundImage = "url('static/img/weatherBackground/background_snow.jpg')";
        document.body.style.color = "black";
        for (var i = 0; i < cards.length; i++){
            cards[i].style.color = "black";
        }
        changeTempCharXYColor("black");
        old_bg = "background_snow.jpg";
        document.getElementById("buttonTempChart").classList.replace("btn-dark", "btn-outline-dark");
        document.getElementById("buttonPercChart").classList.replace("btn-dark", "btn-outline-dark");
        document.getElementById("buttonHumiChart").classList.replace("btn-dark", "btn-outline-dark");

    } else if(weatherKind == "stormy" && old_bg != "background_stormy.jpg"){
        document.body.style.backgroundImage = "url('static/img/weatherBackground/background_stormy.jpg')";
        document.body.style.color = "white";
        for (var i = 0; i < cards.length; i++){
            cards[i].style.color = "white";
        }
        changeTempCharXYColor("white");
        old_bg = "background_stormy.jpg";
        document.getElementById("buttonTempChart").classList.replace("btn-outline-dark", "btn-dark");
        document.getElementById("buttonPercChart").classList.replace("btn-outline-dark", "btn-dark");
        document.getElementById("buttonHumiChart").classList.replace("btn-outline-dark", "btn-dark");

    }else if (old_bg != "Wetter_bg.jpg"){
        document.body.style.backgroundImage = "url('static/img/weatherBackground/Wetter_bg.jpg')";
        document.body.style.color = "white";
        for (var i = 0; i < cards.length; i++){
            cards[i].style.color = "white";
        }
        changeTempCharXYColor("white");
        old_bg = "Wetter_bg.jpg";
        document.getElementById("buttonTempChart").classList.replace("btn-outline-dark", "btn-dark");
        document.getElementById("buttonPercChart").classList.replace("btn-outline-dark", "btn-dark");
        document.getElementById("buttonHumiChart").classList.replace("btn-outline-dark", "btn-dark");
    }
}


function changeTempCharXYColor(colorName){
    /*if (colorName == "white"){
        console.log(chartOptions);
        chartOptions["yAxis"]["labels"]["style"]["colors"] = 'white';
        chart.updateOptions(chartOptions);

    }else if (colorName == "black"){
        chart.foreColor = '#000';
    }else{
        throw "Invalid or not implemented color name!";
    }*/
}

function fillInformations (data){
    let tempWeather = refreshWeather(data["current"]["weather"]["0"]["id"]);
    document.getElementById("todayWeatherTemp").innerHTML = Math.round(data["current"]["temp"]) + "&degC";
    document.getElementById("todayWeatherFeelsLikeTemp").innerHTML = Math.round(data["current"]["feels_like"]) + "&deg";
    document.getElementById("todayWeatherCloudiness").innerHTML = data["current"]["clouds"] + "&percnt;";
    document.getElementById("todayWeatherWindSpeed").innerHTML = data["current"]["wind_speed"] + " km/h";
    document.getElementById("todayWeatherVision").innerHTML = (data["current"]["visibility"]/1000) + "km";
    document.getElementById("todayWeatherHumidity").innerHTML = data["current"]["humidity"] + "&percnt;";
    document.getElementById("todayWeatherDescription").innerHTML = data["current"]["weather"]["0"]["description"];
    document.getElementById("todayWeatherIcon").innerHTML = "<img src=\"static/svg/weatherIcons/"+tempWeather[0]+"\" width=\"175px\">";
    document.getElementById("todayWeatherDew").innerHTML = Math.round(data["current"]["dew_point"]).toString() + "&degC";
    document.getElementById("todayWeatherUVIndex").innerHTML = Math.round(data["current"]["uvi"]);
    refreshBackgroundAndText(tempWeather[1]);
    for(let i = 0; i < 8; i++){
        fillInformationForOneDay(i, data["daily"][i]);
    }
}

function fillInformationForOneDay(daynumber, dayWeather){
    let number = date.getDay() + daynumber;
    let newDayNumber = number % 7;
    if (newDayNumber == 0){
        newDayNumber = 7;
    }
    if (daynumber == 0){
        document.getElementById("day"+daynumber+"-headline").innerHTML = "Heute";
    } else if (daynumber == 1){
        document.getElementById("day"+daynumber+"-headline").innerHTML = "Morgen";
    } else {
        document.getElementById("day"+daynumber+"-headline").innerHTML = getWeekdayName(newDayNumber);
    }
    document.getElementById("day"+daynumber+"-weather-icon").innerHTML = "<img src=\"static/svg/weatherIcons/"+refreshWeather(dayWeather["weather"]["0"]["id"])[0]+"\" width=\"75%\">";
    document.getElementById("day"+daynumber+"-max-temp").innerHTML = Math.round(dayWeather["temp"]["max"]) +"&deg;";
    document.getElementById("day"+daynumber+"-min-temp").innerHTML =Math.round( dayWeather["temp"]["min"]) +"&deg;";
}

function createNextHoursTempChart(data){
    date = new Date();
    let xValues = [];
    let descriptions = [];

    let tempYValues = [];
    let feelsLikeYValues = [];
    let precipitation = [];
    let humidity = [];


    for (let i = 0; i <= forcastCounter; i++){
        tempYValues.push([date.addHours(i), Math.round(data["hourly"][i]["temp"])]);
        feelsLikeYValues.push([date.addHours(i), Math.round(data["hourly"][i]["feels_like"])]);
        humidity.push([date.addHours(i), Math.round(data["hourly"][i]["humidity"])]);
    }
    for(let i = 0; i < 60; i++){
        precipitation.push([date.addMinutes(i), data["minutely"][i]["precipitation"]]);
    }

    for (let i = 1; i < forcastCounter; i++){
        xValues.push(date.addHours(i).getTime());
    }

    chartOptions = {
        chart: {
            theme: "dark",
            type: 'area',
            height: 250,
            fill: {
                type: "gradient",
                gradient: {
                    enabled: true,
                    opacityFrom: 0.55,
                    opacityTo: 0
                }
            },
            zoom: {
                enabled: true
            },
            animations: {
                initialAnimation: {
                    enabled: false
                }
            },
            stroke: {
                curve: 'smooth',
            },
            toolbar: {
                tools: {
                    download: false,
                    selection: false,
                    pan: true,
                    reset: false
                }
            }
        },
        tooltip: {
            enabled: true,
            format: 'HH:mm',
            theme: "dark",
            x: {
                formatter: function(value, { series, seriesIndex, dataPointIndex, w }) {
                    let tempTime = new Date(value);
                    let min = tempTime.getMinutes().toString();
                    if (min.length < 2){
                        min = "0" + min;
                    }
                    return tempTime.getHours() + ":" + min;
                }
            }
        },
        legend: {
            show: false
        },
        series: [{
            name: "Temperatur",
            data: tempYValues
        }, {
            name: "gefühlt",
            data: feelsLikeYValues
        }, {
            name: "Niederschlag",
            data: precipitation
        }, {
            name: "Luftfeuchtigkeit",
            data: humidity
        }
        ],
        yaxis: {
            forceNiceScale: true,
            min: 0,
            labels: {
                formatter: function (value) {
                return value + " °C";
                },
                style: {
                    colors: "white",
                    fontWeight: "bold"
                }
            },
        },
        xaxis: {
            type: 'datetime',
            categories: xValues,
            labels: {
                style: {
                  colors: "white",
                  fontWeight: "bold"
                }
            }
        }
      };

    chart = new ApexCharts(document.getElementById("myChart"), chartOptions);
    chart.render();
    chart.zoomX(xValues[0], xValues[12]);
    chart.hideSeries('gefühlt');
    chart.hideSeries('Niederschlag');
    chart.hideSeries('Luftfeuchtigkeit');
    chart.updateOptions({animate: false});
    chartOptions = chart.options;
}

Date.prototype.addHours = function(h){
    var copiedDate = new Date(this.getTime());
    copiedDate.setHours(copiedDate.getHours()+h);
    //copiedDate.setMinutes(0);
    return copiedDate;
}

Date.prototype.addMinutes = function(m){
    var copiedDate = new Date(this.getTime());
    copiedDate.setMinutes(copiedDate.getMinutes()+m);
    return copiedDate;
}

function showChartContenTemp(){
    document.getElementById("buttonTempChart").classList.add("active");
    document.getElementById("buttonPercChart").classList.remove("active");
    document.getElementById("buttonHumiChart").classList.remove("active");

    activeChart = "temperatur";

    let tempOptions = chartOptions;
    let xValues = [];

    for (let i = 1; i < forcastCounter; i++){
        xValues.push(date.addHours(i).getTime());
    }

    tempOptions["yaxis"] = {
        forceNiceScale: true,
        min: 0,
        labels: {
            formatter: function (value) {
            return value + " °C";
            },
            style: {
                colors: "white"
            }
        }
    };
    tempOptions["xaxis"] = {
        type: 'datetime',
        categories: xValues,
        tickPlacement: 'on',
        labels: {
            style: {
              colors: "white",
              fontWeight: "bold"
            }
        }
    };
    chart.updateOptions(tempOptions);

    chart.hideSeries('Niederschlag');
    chart.hideSeries('Luftfeuchtigkeit');
    chart.hideSeries('gefühlt');
    chart.showSeries("Temperatur");
    chart.zoomX(xValues[0], xValues[11]);

    document.getElementById("chartForecastHeadline").innerHTML = "48-Stunden-Vorhersage";
}

function showChartContenPerc(){
    document.getElementById("buttonTempChart").classList.remove("active");
    document.getElementById("buttonPercChart").classList.add("active");
    document.getElementById("buttonHumiChart").classList.remove("active");

    activeChart = "percipitation";

    let xValues = [];
    let tempOptions = chartOptions;
    date = new Date();

    for (let i = 0; i < 60; i++){
        xValues.push(date.addMinutes(i));
    }

    tempOptions["yaxis"] = {
        forceNiceScale: true,
        min: 0,
        labels: {
            formatter: function (value) {
            return Math.round(value *1000)/1000 + " mm";
            },
            style: {
                colors: "white",
                "fontWeight": "bold"
            }
        }
    };
    tempOptions["xaxis"] = {
        type: 'datetime',
        categories: xValues,
        tickPlacement: 'on',
        labels: {
            style: {
              colors: "white",
              fontWeight: "bold"
            }
        }
    };

    chart.hideSeries('Temperatur');
    chart.hideSeries('Luftfeuchtigkeit');
    chart.hideSeries('gefühlt');
    chart.showSeries("Niederschlag");
    chart.updateOptions(tempOptions);
    chart.zoomX();
    document.getElementById("chartForecastHeadline").innerHTML = "60-Minuten-Vorhersage";

}

function showChartContenHumi(){
    document.getElementById("buttonTempChart").classList.remove("active");
    document.getElementById("buttonPercChart").classList.remove("active");
    document.getElementById("buttonHumiChart").classList.add("active");

    activeChart = "humidity";

    let tempOptions = chartOptions;
    let xValues = [];

    for (let i = 1; i < forcastCounter; i++){
        xValues.push(date.addHours(i).getTime());
    }

    tempOptions["yaxis"] = {
        forceNiceScale: true,
        min: 0,
        labels: {
            formatter: function (value) {
            return value + "%";
            },
            style: {
                colors: "white",
                fontWeight: "bold"
            }
        }
    };
    tempOptions["xaxis"] = {
        type: 'datetime',
        categories: xValues,
        tickPlacement: 'on'
    };
    chart.updateOptions(tempOptions);

    chart.hideSeries('Niederschlag');
    chart.hideSeries('Temperatur');
    chart.hideSeries('gefühlt');
    chart.showSeries("Luftfeuchtigkeit");
    chart.zoomX(xValues[0], xValues[11]);
    document.getElementById("chartForecastHeadline").innerHTML = "48-Stunden-Vorhersage";
}

function updateNextTwoHourPrediction(data, offset){
    let xValues = [];

    let tempYValues = [];
    let feelsLikeYValues = [];
    let precipitation = [];
    let humidity = [];


    for (let i = 1; i <= forcastCounter; i++){
        let tempTime = date.addHours(i).getTime();
        tempYValues.push([tempTime, Math.round(data["hourly"][i]["temp"])]);
        feelsLikeYValues.push([tempTime, Math.round(data["hourly"][i]["feels_like"])]);
        humidity.push([tempTime, Math.round(data["hourly"][i]["humidity"])]);
    }

    for(let i = 0; i < 60; i++){
        precipitation.push([date.addMinutes(i).getTime(), data["minutely"][i]["precipitation"]]);
    }

    if (activeChart == "percipitation"){
        console.log("perc");
        for (let i = 0; i < 60; i++){
            xValues.push(date.addMinutes(i).getTime());
        }
    } else {
        for (let i = 1; i < forcastCounter; i++){
            xValues.push(date.addHours(i).getTime());
        }
    }
    chart.updateOptions([{
        series: [{
            name: "Temperatur",
            data: tempYValues
        }, {
            name: "gefühlt",
            data: feelsLikeYValues
        }, {
            name: "Niederschlag",
            data: precipitation
        }, {
            name: "Luftfeuchtigkeit",
            data: humidity
        }
        ],
        xaxis: {
            type: 'datetime',
            categories: xValues,
            tickPlacement: 'on'
        }
        }]);

    if (activeChart == "percipitation"){
        chart.zoomX(xValues[0], xValues[59]);
    } else {
        chart.zoomX(xValues[0], xValues[12]);
    }

}


function createDailyWeatherWidgets(anzDays, data){
    let output = "";
    for (let i = 0; i < anzDays; i++){
        if (i == activeDayCard){
            output += "<button class=\"day-card btn btn-outline-dark col\" data-toggle=\"modal\" data-target=\"#day"+i+"-modal\">";
        }else {
            output += "<button class=\"day-card btn btn-outline-dark col\" data-toggle=\"modal\" data-target=\"#day"+i+"-modal\">";
        }
        output += " <div class=\"d-flex flex-column\">";
        output += "<div class=\"day-card-headline\" id=\"day"+i+"-headline\">";
        if (i == 0){
            output += "Heute";
        }else if (i == 1){
            output += "Morgen";
        }else {
            let newDayNumber = (date.getDay()+i) % 7;
            if (newDayNumber == 0){
                newDayNumber = 7;
            }
            output += getWeekdayName(newDayNumber);
        }
        output += "</div>";
        output += "<div class=\"day-card-weather-icon\" id=\"day"+i+"-weather-icon\">";
        output += "</div>";
        output += "<div class=\"day-card-temp-section\">";
        output += "<span class=\"material-icons-round\">arrow_drop_up</span><span id=\"day"+i+"-max-temp\"></span><br />";
        output += "<span class=\"material-icons-round\">arrow_drop_down</span><span id=\"day"+i+"-min-temp\"></span>";
        output += "</div>";
        output += "</div>";
        output += "</button>";
        output += "\n";
    }

    document.getElementById("nextDaysRow").innerHTML = output;

    for (let i = 0; i < anzDays; i++){
        fillInformationForOneDay(i, data["daily"][i]);
    }
}

function getWeekdayName(tempDateNumber){
    if (tempDateNumber == 1){
        return "Montag";
    }else if (tempDateNumber == 2){
        return "Dienstag";
    }else if (tempDateNumber == 3){
        return "Mittwoch";
    }else if (tempDateNumber == 4){
        return "Donnerstag";
    }else if (tempDateNumber == 5){
        return "Freitag";
    }else if (tempDateNumber == 6){
        return "Samstag";
    }else if (tempDateNumber == 7){
        return "Sonntag";
    }else {
        throw "invalid parameter!";
    }
}

function refresh(){
    date = new Date();
    console.log("refreshing...");
    $.getJSON("https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&appid="+apiKey+"&lang=de&units=metric", function(data){
        createDayModals(8, data);
        if (chart == null){
            createNextHoursTempChart(data);
        }else {
            updateNextTwoHourPrediction(data, 0);
        }
        fillInformations(data);
    });
}

function createDayModals(anzDays, data){
    let modalCode = "";
    for(let i = 0; i < anzDays; i++){
        let weatherInf = refreshWeather(data["daily"][i]["weather"]["0"]["id"]);
        modalCode += "<div class=\"modal fade\" id=\"day"+i+"-modal\">";
        modalCode += "<div class=\"modal-dialog modal-dialog-centered modal-lg\" style=\"\"><div class=\"modal-content\"><div class=\"modal-header\">";
        modalCode += "<div class=\"modal-title\" id=\"day"+i+"-modalTitle\">";
        let newDayNumber = (date.getDay()+i) % 7;
        if (newDayNumber == 0){
            newDayNumber = 7;
        } else{
            modalCode += getWeekdayName(newDayNumber);
        }
        modalCode += "<button type=\"button\" class=\"close\" data-dismiss=\"modal\">&times;</button></div></div>";
        modalCode += "<div class=\"modal-body\" id=\"day"+i+"-modalBody\" style=\"color: rgb(0, 0, 0)\">";
        modalCode += "<div class=\"row\">";
        modalCode += "<div class=\"col\" id=\"day"+i+"-modal-weather-icon\">";
        modalCode += "<img src=\"static/svg/weatherIcons/"+weatherInf[0]+"\" width=\"175px\">";
        modalCode += "</div>";
        modalCode += "<div class=\"col\" id=\"day"+i+"-modal-descr\" style=\"font-size: 3em\">";
        modalCode += data["daily"][i]["weather"]["0"]["description"];
        modalCode += "</div>";
        modalCode += "<div class=\"col\" id=\"day"+i+"-modal-temp\">";
        modalCode += "<span class=\"material-icons-round\">arrow_drop_up</span><span id=\"day"+i+"-max-temp\">"+Math.round(data["daily"][i]["temp"]["max"])+" &degC</span><br />";
        modalCode += "<span class=\"material-icons-round\">arrow_drop_down</span><span id=\"day"+i+"-min-temp\">"+Math.round(data["daily"][i]["temp"]["min"])+" &degC</span>";
        modalCode += "</div>";
        modalCode += "</div>";
        modalCode += "<div class=\"row justify-content-around\" style=\"margin-bottom: 20px\"><div class=\"col details\"><span class=\"material-icons-outlined\">air</span><span class=\"flex-column detail-headline\">";
        modalCode += "<div>Wind</div><div class=\"detail-value\" id=\"day"+i+"-WeatherWindSpeed\">"+data["daily"][i]["wind_speed"]+" km/h</div>";
        modalCode += "</span></div>";
        modalCode += "<div class=\"col details\"><span class=\"material-icons-outlined\">cloud</span><span class=\"detail-headline\">";
        modalCode += "<div>Wolken</div><div class=\"detail-value\" id=\"day"+i+"-WeatherVision\">"+data["daily"][i]["clouds"]+"%</div></span></div>";

        modalCode += "<div class=\"col details\"><span class=\"material-icons-outlined\">water_drop</span><span class=\"detail-headline\">";
        modalCode += "<div>Luftfeuchtigkeit</div><div class=\"detail-value\" id=\"day"+i+"-WeatherVision\">"+data["daily"][i]["humidity"]+"%</div></span></div>";

        modalCode += "<div class=\"col details\"><span class=\"material-icons-outlined\">ac_unit</span><span class=\"detail-headline\">";
        modalCode += "<div>Taupunkt</div><div class=\"detail-value\" id=\"day"+i+"-WeatherVision\">"+Math.round(data["daily"][i]["dew_point"])+" &degC</div></span></div>";
        modalCode += "<div class=\"col details\"><span class=\"material-icons-outlined\">wb_sunny</span><span class=\"detail-headline\">";
        modalCode += "<div>UV-Index</div><div class=\"detail-value\" id=\"day"+i+"-WeatherVision\">"+data["daily"][i]["uvi"]+"</div></span></div>";
        modalCode += "</div>";
        modalCode += "<div class=\"modal-footer\">";
        modalCode += "<button type=\"button\" class=\"btn btn-danger\" data-dismiss=\"modal\">Schließen</button>";
        modalCode += "</div></div></div></div></div>";
    }
    document.getElementById("dailyModals").innerHTML = modalCode;
}

document.getElementById("state").innerHTML = ipAPI.city.replace(/(\s)/gi, "+"); // Replace spaces
lat = 49.783333;
lon = 9.933333;
$.getJSON("https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&appid="+apiKey+"&lang=de&units=metric", function(data){
    createDailyWeatherWidgets(8, data);
});
refresh();
setInterval(refresh, 30000);

$.getJSON("https://ipapi.co/json/", function(ipAPI) {
    lat = ipAPI.latitude;
    lon = ipAPI.longitude;
    document.getElementById("state").innerHTML = ipAPI.city.replace(/(\s)/gi, "+"); // Replace spaces

    date = new Date();
    $.getJSON("https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&appid="+apiKey+"&lang=de&units=metric", function(data){
        createDailyWeatherWidgets(8, data);
    });
    refresh();
    setInterval(refresh, 30000);
}).done();


var old_bg = "";
var activeDayCard = 0;
var apiKey = "bd4d17c6eedcff6efc70b9cefda99082";
var date;
var lat;
var lon;

var chart = null;
var chartOptions = null;
const forcastCounter = 47;
var activeChart = "temparatur";

var tempGraphVisible = true;
var percGraphVisible = false;
var humiGraphVisible = false;
