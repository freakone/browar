<!DOCTYPE html>
<html>
<head>
  <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.4.min.js"></script>
  <script type="text/javascript">
    var ws = new WebSocket("ws://kaliszfornia.brewit.pl/ws");
    ws.onmessage = function (evt) {
        json = JSON.parse(evt.data)
        console.log(json);
        $('span.gora').html(json['gora']);
        $('span.dol').html(json['dol']);
    };
  </script>
</head>
<body>
<ul>
    <li>Temperatura górna <span class="gora">0</span></li>
    <li>Temperatura dół <span class="dol">0</span></li>
</ul> 
</body>
</html>
