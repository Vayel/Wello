(function() {
    var tankCanvas = document.querySelector('#tank_canvas');

    function updateWaterVolume(volume) {
        if (volume === 'undefined' || volume == null) {
            tankCanvas.style.display = 'none';
            return document.querySelector('#unknown_water_volume').style.display = 'block';
        }
        tankCanvas.style.display = 'block';
        document.querySelector('#unknown_water_volume').style.display = 'none';

        var el = document.querySelector('#water_volume');
        el.innerHTML = volume; 

        if(volume < MIN_VOLUME) {
            el.className = 'underflow';
        } else if(volume > MAX_VOLUME) {
            el.className = 'overflow';
        } else {
            el.className = '';
        }

        drawTankCanvas(volume / TOTAL_VOLUME, MAX_WATER_PERCENTAGE, MIN_WATER_PERCENTAGE);
    }

    function drawTankCanvas(waterPercentage, maxWaterPercentage, minWaterPercentage) {
        var ctx = tankCanvas.getContext('2d');

        ctx.clearRect(0, 0, tankCanvas.width, tankCanvas.height);

        var waterHeight = tankCanvas.height * waterPercentage;
        ctx.fillStyle = 'blue';
        ctx.fillRect(0, tankCanvas.height - waterHeight, tankCanvas.width, tankCanvas.height);
        
        var maxHeight = tankCanvas.height * (1 - maxWaterPercentage);
        ctx.beginPath();
        ctx.moveTo(0, maxHeight);
        ctx.lineTo(tankCanvas.width, maxHeight);
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 2;
        ctx.stroke();

        var minHeight = tankCanvas.height * (1 - minWaterPercentage);
        ctx.beginPath();
        ctx.moveTo(0, minHeight);
        ctx.lineTo(tankCanvas.width, minHeight);
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.lineWidth = 2;
        ctx.strokeRect(0, 0, tankCanvas.width, tankCanvas.height);
    }

    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {});
    socket.on('pump_in_state', function(msg) {
      document.querySelector('#pump_in_state').innerHTML = msg.running; 
    });
    socket.on('urban_network_state', function(msg) {
      document.querySelector('#urban_network_state').innerHTML = msg.running; 
    });
    socket.on('error', function(msg) {
      var li = document.createElement("li");
      var now = new Date();
      li.innerHTML = "[" + now.toISOString().substring(0, 19).split("T").join(" ") + "]: " + msg.text;
      document.querySelector('.flashes').appendChild(li);
    });
    socket.on('water_volume', function(msg) {
        updateWaterVolume(msg.volume);
    });
    socket.on('water_flow_in', function(msg) {
      var el = document.querySelector('#water_flow_in');
      el.innerHTML = msg.value; 

      if(msg.volume < MIN_FLOW_IN) {
          el.className = 'underflow';
      } else {
          el.className = '';
      }
    });
    socket.on('water_flow_out', function(msg) {
      var el = document.querySelector('#water_flow_out');
      el.innerHTML = msg.value; 
    });

    updateWaterVolume(WATER_VOLUME);
})();
