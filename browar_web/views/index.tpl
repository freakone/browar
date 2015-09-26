<!DOCTYPE html>
<html>

<head>
    <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.4.min.js"></script>
    <script type="text/javascript" src="http://www.chartjs.org/assets/Chart.min.js"></script>

    <script type="text/javascript">
        var lineChartData = {
            labels: [],
            datasets: [
            {
              label: "Fermentor",
              fillColor : "rgba(220,220,220,0.2)",
              strokeColor : "rgba(220,220,220,1)",
              pointColor : "rgba(220,220,220,1)",
              pointStrokeColor : "#fff",
              pointHighlightFill : "#fff",
              pointHighlightStroke : "rgba(220,220,220,1)",
              data : []
            },
            {
                label: "Beczka",
                fillColor: "rgba(151,187,205,0.2)",
                strokeColor: "rgba(151,187,205,1)",
                pointColor: "rgba(151,187,205,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(151,187,205,1)",
                data: []
            },
            {
                label: "Pompa",
                fillColor: "rgba(170, 44, 44, 0.9)",
                strokeColor: "rgba(170, 44, 44, 0.9)",
                pointColor: "rgba(170, 44, 44, 0.9)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(170, 44, 44, 0.9)",
                data: []
            },
            {
                label: "Kompresor",
                fillColor: "rgba(170, 198, 44, 0.9",
                strokeColor: "rgba(170, 198, 44, 0.9)",
                pointColor: "rgba(170, 198, 44, 0.9)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(170, 198, 44, 0.9)",
                data: [],
            }],


        }

        var pompa = function() {
            ws.send(JSON.stringify({
                action: "pump"
            }));
        }

        var sprezarka = function() {
            ws.send(JSON.stringify({
                action: "compressor"
            }));
        }

        var set_dest = function() {
            ws.send(JSON.stringify({
                action: "set_dest",
                beczka: $('#dest_beczka').val(),
                fermentor: $('#dest_fermentor').val()
            }));
        }

        var ws = new WebSocket("ws://kaliszfornia.brewit.pl/ws");
        ws.onmessage = function(evt) {
            json = JSON.parse(evt.data);
            console.log(json);
            switch (json["action"]) {
                case "init":
                    json["data"].forEach(function(item) {
                        lineChartData.labels.push(item[0])
                        lineChartData.datasets[0]["data"].push(item[1])
                        lineChartData.datasets[1]["data"].push(item[2])
                        lineChartData.datasets[2]["data"].push(item[4]*2)
                        lineChartData.datasets[3]["data"].push(item[5])
                        $('span.gora').html(item[1]);
                        $('span.dol').html(item[2]);
                    });

                    var ctx = document.getElementById("canvas").getContext("2d");
                    window.myLine = new Chart(ctx).Line(lineChartData, {
                        responsive: true,
                        legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"
                    });

                    $('#legend').append(window.myLine.generateLegend());


                    break;
                case "add":
                    $('span.gora').html(json['ext']);
                    $('span.dol').html(json['beczka']);
                    window.myLine.addData([json['ext'], json['beczka'], json['pompa']*2, json['sprezarka']], json['time'])

                    break;

                case "state":
                    $('span.pompa').html(json['pompa']);
                    $('span.sprezarka').html(json['sprezarka']);
                    break;

                case "set_dest":
                    $('#dest_beczka').val(json['beczka']);
                    $('#dest_fermentor').val(json['fermentor']);
                    $('span.change').html(" Zmieniono nastawy")
                    setTimeout(function(){
                      $('span.change').html("")
                    }, 2000);
                    break;
            }
        };
    </script>

    <style type="text/css">
    .line-legend li span{
        display: inline-block;
        width: 12px;
        height: 12px;
        margin-right: 5px;
    }
    #legend ul li{
        display: inline;
        margin-right: 10px;
    }
    </style>
</head>

<body>
    <ul>
        <li>Pompa <span class="pompa">OFF</span>
            <button onclick="pompa()">TOGGLE</button>
        </li>
        <li>Sprezarka <span class="sprezarka">OFF</span>
            <button onclick="sprezarka()">TOGGLE</button>
        </li>
        <li>Temperatura fermentor <span class="gora">0</span></li>
        <li>Temperatura beczka <span class="dol">0</span></li>
        <li>Docelowo - beczka <input id="dest_beczka" type="number" min="1" max="25" step="1"></li>
        <li>Docelowo - fermentor <input id="dest_fermentor" type="number" min="1" max="25" step="1"></li>
        <li><button onclick="set_dest()">Ustaw regulator</button><span class="change"></span></li>
    </ul>

    <div id ="legend"></div>

    <div style="width:70%">
        <div>
            <canvas id="canvas" height="450" width="600"></canvas>
        </div>
    </div>


</body>

</html>