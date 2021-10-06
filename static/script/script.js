let ss = 0;
let mm = 0;
let hh = 0;
let seconds = 0;
let minutes = 0;
let hours = 0;
let interval = null;
let status = "stopped";

function showTime() {
  hours = hh;
  if (mm < 10) {
    minutes = "0" + mm.toString();
  }
  else {
    minutes = mm;
  }
  if (ss < 10) {
    seconds = "0" + ss.toString();
  }
  else {
    seconds = ss;
  }
}

function increment() {
  ss++;
  if (ss == 60) {
    mm++;
    ss = 0;
    if (mm == 60) {
      hh++;
      mm = 0;
    }
  }
  showTime();
  document.getElementById("display").innerHTML = hours + ":" + minutes + ":" + seconds;
}

function startTimer() {
  if (status == "stopped") {
    ss = 0;
    mm = 0;
    hh = 0;
    showTime();
    document.getElementById("display").innerHTML = hours + ":" + minutes + ":" + seconds;
    interval = window.setInterval(increment, 1000);
    status = "started";

  }
}

function endTimer() {
  if (status == "started") {
    window.clearInterval(interval);
    status = "stopped";
    showTime();

    addRemoteTime();
   }
 }


function clearTimer() {
   if (status == "started") {
        endTimer();
   }

    if (confirm("Clear all times?")) {
        clearRemoteTimes();
    }

}

function addRemoteTime() {
    $.ajax({
        type: 'POST',
        url:'/addTime',
        data: '{"time": "' + hours + ':' + minutes + ':' + seconds + '"}',
        success: function(msg){
            getRemoteTimes();
        }
    });
}


function getRemoteTimes() {
    document.querySelector('ul').innerHTML = "";

     $.get( "/getTimes", function( data ) {
          $.each(data, function(i){
                 var node = document.createElement('li');
                 node.appendChild(document.createTextNode(data[i]));
                 document.querySelector('ul').appendChild(node);
              })

      });
}

function clearRemoteTimes() {
     $.get( "/clearTimes", function( data ) {
          getRemoteTimes();
      });
}

