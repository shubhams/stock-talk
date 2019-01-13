$('.js-data-example-ajax').select2({
    minimumInputLength: 3,
    placeholder: 'Type a symbol',
    allowClear: true,
    ajax: {
        url: '/search',
        delay: 250,
        data: function (params) {
            return {
                sym: params.term
            };
        },
        cache: true
    }
});

function submitSymbol(csrfToken) {
    var val = $('.js-data-example-ajax').val();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("save-response").innerHTML = this.responseText;
        }
    };
    xhttp.open("POST", "/save", true);
    xhttp.setRequestHeader("X-CSRFToken", csrfToken);
    var postData = new FormData();
    postData.append('sym', val);
    xhttp.send(postData);
}

function submitDelete(csrfToken, sym) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("save-response").innerHTML = this.responseText;
        }
    };
    xhttp.open("POST", "/remove", true);
    xhttp.setRequestHeader("X-CSRFToken", csrfToken);
    var postData = new FormData();
    postData.append('sym', sym);
    xhttp.send(postData);
}

function submitLogout(csrfToken) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/logout", true);
    xhttp.setRequestHeader("X-CSRFToken", csrfToken);
    xhttp.send();
}

function render_chart(id) {
    var dataPoints = [];
    var chart = new CanvasJS.Chart(id,{
        title:{
            text:"Stock Price of " + id
        },
        data: dataPoints,
        axisX: {
            title: "Days",
        },
        axisY: {
            title: "Points",
        }
    });
    url = "/timeseries?sym="+id;
    var openPoints = [];
    var highPoints = [];
    var lowPoints = [];
    var closePoints = [];
    var openLine = {};
    var highLine = {};
    var lowLine = {};
    var closeLine = {};
    $.getJSON(url, function(data) {
        $.each(data['Time Series (60min)'], function(key, value){
            // openPoints.push({x: new Date(key), y: parseFloat(value['1. open'])});
            highPoints.push({x: new Date(key), y: parseFloat(value['2. high'])});
            lowPoints.push({x: new Date(key), y: parseFloat(value['3. low'])});
            // closePoints.push({x: new Date(key), y: parseFloat(value['4. close'])});
        });
        // openLine['type'] = 'line';
        highLine['type'] = 'spline';
        lowLine['type'] = 'spline';
        // closeLine['type'] = 'line';

        // openLine['name'] = 'open';
        highLine['name'] = 'high';
        lowLine['name'] = 'low';
        // closeLine['name'] = 'close';

        // openLine['showInLegend'] = true;
        highLine['showInLegend'] = true;
        lowLine['showInLegend'] = true;
        // closeLine['showInLegend'] = true;

        // openLine['dataPoints'] = openPoints;
        highLine['dataPoints'] = highPoints;
        lowLine['dataPoints'] = lowPoints;
        // closeLine['dataPoints'] = closePoints;

        dataPoints.push(highLine, lowLine);
        chart.render();
    });
}


window.onload = function () {
    var ids = $('.chart-container').map(function(){
        return this.id;
    }).get();
    for (i in ids) {
        render_chart(ids[i]);
    }
};
