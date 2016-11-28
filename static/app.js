// load function should be called in beginning as it is loaded once
    google.charts.load('44', {'packages':['corechart']});

    document.getElementById('loader').style.visibility = "hidden";
    function updateTextInput1(val) {
              document.getElementById('textInput1').value=val;
            }

    function updateTextInput2(val) {
              document.getElementById('textInput2').value=val;
            }

//helper for dropdown
function initDropdownList( id, a) {

    //controls
    var select, i, option;
    select = document.getElementById( id );

    for ( i = 0; i < a.length; i += 1 ) {
        option = document.createElement( 'option' );
        option.value = i
        option.text = a[i];
        select.add( option );
    }
}

//upload a file when user chooses it
document.getElementById("file").onchange = function() {

  //controls
  $(".spi").show();
  console.log("FILE ");
  document.getElementById('loader').style.visibility = "visible";
  var data = new FormData()
  data.append('file', document.getElementById('file').files[0]);

  //upload a file
  axios.post('/upload', data)
       .then(function (res) {
          var filename = document.getElementById('file').files[0].name
          window.localStorage.setItem('current', filename);
          document.getElementById('loader').style.visibility = "hidden";

          //get list of ip's
          if(window.localStorage.getItem('current') != null){
          var filen = window.localStorage.getItem('current').split('.')
          axios.post('/listOfIp/'+filen[0]+'.csv')
               .then(function (res) {
                 initDropdownList('ip',res.data.ip)
               })
               .catch(function (err) {
                 toastr.error("Error occured in retrieving IP's");
               })

            }

          toastr.success('File uploaded')
        })
        .catch(function (err) {
          toastr.error("Error occured");
        })
}

//function to plot the detected outliers
function detect() {
      //clear the initial content
      document.getElementById('chart').innerHTML = "";
      //get the selected algo
      var ev = document.getElementById('algo')
      var selectedAlgo = ev.options[ev.selectedIndex].value
    switch (parseInt(selectedAlgo)) {
      case 0: IQR();
        break;
      case 1: MMedian();
        break;
      case 2: MAvg();
        break;
      default:
        toastr.error("Select appropriate choice")
      }
    }

    function googleChartHelper(res) {
      var dataTable = [];

      // prepare the dataTable for google charts
      dataTable.push(['timestamp',
                      'RequestHits',
                      {'type': 'string', 'role': 'style'},
                      {'type': 'string', 'role': 'tooltip'}])
      for(var i = 0;i < res.data.inliers.length;i++) {
           var arr = [];
           arr.push(res.data.inliers[i].x);
           arr.push(res.data.inliers[i].y);
           arr.push('point { fill-color: 	#006400; }');
           arr.push(res.data.inliers[i]["time"] +
                   " : " + (res.data.inliers[i].y).toString());
           dataTable.push(arr);
      }
      for(var k =0;k < res.data.outliers.length;k++) {
           var arr = [];
           arr.push(res.data.outliers[k].x);
           arr.push(res.data.outliers[k].y);
           arr.push('point { fill-color: #ff0000; }');
           arr.push(res.data.outliers[k]["time"] +
                   " : " + (res.data.outliers[k].y).toString());
           dataTable.push(arr);
      }

        google.charts.setOnLoadCallback(drawChart);

       //helper to customize google charts and plot ScatterChart
       function drawChart() {
         var data = google.visualization.arrayToDataTable(dataTable);

         var options = {
           title: 'request counts vs timestamp',
           legend: 'right',
           width: 1000,
           height: 400,
           chartArea: {
             backgroundColor: {
               stroke: '#4322c0',
               strokeWidth: 3
             }
           },
           explorer: {
             actions: ['dragToZoom', 'rightClickToReset'],
             axis: 'horizontal',
             keepInBounds: true,
             maxZoomIn: 4.0
     }
         };

         var chart = new google.visualization.ScatterChart(document.getElementById('chart'));

         chart.draw(data, options);
       }
    }

    //InterQuartile Range
    function IQR() {

        //controls
        var e = document.getElementById("ip");
        var selectedIp = e.options[e.selectedIndex].text;
        var filen = window.localStorage.getItem('current').split('.')
        var filename = filen[0]+".csv"

        //post data
        var data = {
          ip : selectedIp,
          alpha : parseFloat(document.getElementById('textInput1').value),
          filename : filename
        }
          axios.post('/interq', data)
               .then(function(res) {
                 googleChartHelper(res);
               })
               .catch(function(err) {
                 console.log(err);
               })
    }

    // Moving Median Absolute Deviation
    function MMedian() {

        //controls
        var e = document.getElementById("ip");
        var selectedIp = e.options[e.selectedIndex].text;
        var filen = window.localStorage.getItem('current').split('.')
        var filename = filen[0]+".csv"

        //post data
        var data = {
          ip : selectedIp,
          alpha : parseFloat(document.getElementById('textInput1').value),
          filename : filename,
          window_size : parseInt(document.getElementById('textInput2').value)
        }
          axios.post('/movmedian', data)
               .then(function(res) {
                 googleChartHelper(res);
               })
               .catch(function(err) {
                 console.log(err);
               })
    }


        //moving average
    function MAvg() {
          var e = document.getElementById("ip");
          var selectedIp = e.options[e.selectedIndex].text;

          var filen = window.localStorage.getItem('current').split('.')

          var filename = filen[0]+".csv"
          var data = {
            ip : selectedIp,
            filename : filename,
            window_size : parseInt(document.getElementById('textInput2').value)
          }
            axios.post('/movaverage', data)
                 .then(function(res) {
                    googleChartHelper(res);
                 })
                 .catch(function(err) {
                   console.log(err);
                 })
        }

function predict() {
    console.log("HI");
}

$("#outdetect").hide();
$("#outpredict").hide();
$(".spi").hide();

$("#odetect").click(function () {
  $("#outdetect").show();
  $("#outpredict").hide();
});

$("#opredict").click(function () {
  $("#outpredict").show();
  $("#outdetect").hide();
});
