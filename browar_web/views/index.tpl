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
              label: "Beczka",
              fillColor : "rgba(220,220,220,0.2)",
              strokeColor : "rgba(220,220,220,1)",
              pointColor : "rgba(220,220,220,1)",
              pointStrokeColor : "#fff",
              pointHighlightFill : "#fff",
              pointHighlightStroke : "rgba(220,220,220,1)",
              data : []
            },
            {
                label: "Fermentor",
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
                data: []
            }]

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
                        lineChartData.datasets[2]["data"].push(item[4])
                        lineChartData.datasets[3]["data"].push(item[5]*2)
                        $('span.gora').html(item[1]);
                        $('span.dol').html(item[2]);
                    });

                    var ctx = document.getElementById("canvas").getContext("2d");
                    window.myLine = new Chart(ctx).Line(lineChartData, {
                        responsive: true
                    });


                    break;
                case "add":
                    $('span.gora').html(json['ext']);
                    $('span.dol').html(json['beczka']);
                    window.myLine.addData([json['ext'], json['beczka'], json['pompa'], json['sprezarka']*2], json['time'])

                    break;

                case "state":
                    $('span.pompa').html(json['pompa']);
                    $('span.sprezarka').html(json['sprezarka']);
                    break;
            }
        };
    </script>
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
    </ul>

    <div style="width:70%">
        <div>
            <canvas id="canvas" height="450" width="600"></canvas>
        </div>
    </div>


</body>

</html>