var normal_chart, lz4_chart;
lz4_json = null;
normal_json = null;

function lz4_setup() {
    var lz4_output = document.getElementById("lz4_output");
    var lz4_json = null;
    var lz4_request = new XMLHttpRequest();

    lz4_request.open("GET", "/static/js/0004_lz4_output.json", true);
    lz4_request.onreadystatechange = function() {
        if (lz4_request.readyState==4 && lz4_request.status==200) {
            var _lz4_json = JSON.parse(lz4_request.responseText);
            lz4_json = _lz4_json.map(function(x) {
                return [parseInt(x[0]), parseInt(x[1])];
            });
            lz4_chart = new Highcharts.Chart({
                chart: {
                    renderTo: 'lz4_output',
                },
                title: {
                    text: "Memory Usage of OlegDB (LZ4 Compression)"
                },
                yAxis: {
                    title: {
                        text: "Memory Usage (kB)"
                    }
                },
                xAxis: {
                    type: 'datetime'
                },
                series: [{
                    name: "Memory Usage (kB)",
                    color: "#EC757C",
                    data: lz4_json
                }]
            });
            both_setup();
        }
    }
    lz4_request.send();
}

function normal_setup() {
    var normal_json = null;
    var normal_request = new XMLHttpRequest();

    normal_request.open("GET", "/static/js/0004_normal_output.json", true);
    normal_request.onreadystatechange = function() {
        if (normal_request.readyState==4 && normal_request.status==200) {
            var _normal_json = JSON.parse(normal_request.responseText);
            normal_json = _normal_json.map(function(x) {
                return [parseInt(x[0]), parseInt(x[1])];
            });
            normal_chart = new Highcharts.Chart({
                chart: {
                    renderTo: 'normal_output',
                },
                title: {
                    text: "Memory Usage of OlegDB (No LZ4 Compression)"
                },
                yAxis: {
                    title: {
                        text: "Memory Usage (kB)"
                    }
                },
                xAxis: {
                    type: 'datetime'
                },
                series: [{
                    name: "Memory Usage (kB)",
                    data: normal_json
                }]
            });
            both_setup();
        }
    }
    normal_request.send();
}

function both_setup() {
    if (lz4_json == null || normal_json == null)
        return;

    var both_chart = new Highcharts.Chart({
        chart: {
            renderTo: 'both_output',
        },
        title: {
            text: "Memory Usage of OlegDB"
        },
        yAxis: {
            title: {
                text: "Memory Usage (kB)"
            }
        },
        xAxis: {
            type: 'datetime'
        },
        series: [{
            name: "Memory Usage (kB)",
            data: normal_json
        }, {
            name: "Memory Usage (kB)",
            color: "#EC757C",
            data: lz4_json
        }]
    });
}

window.onload = function() {
    lz4_setup();
    normal_setup();
}
