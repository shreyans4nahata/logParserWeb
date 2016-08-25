document.getElementById('loader').style.visibility = "hidden";
function updateTextInput1(val) {
          document.getElementById('textInput1').value=val;
        }

function updateTextInput2(val) {
          document.getElementById('textInput2').value=val;
        }

//helper for dropdown
function initDropdownList( id, a) {
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
function draw(inlier, outlier){
var graph = new Rickshaw.Graph({
        element: document.querySelector("#chart"),
        renderer: 'scatterplot',
        width: 1000,
        height: 485,
        series: [{
                data: inlier,
                color: 'steelblue'
        }, {
                data: outlier,
                color: 'red'
        }]
});
graph.render();
var xAxis = new Rickshaw.Graph.Axis.Time({
    graph: graph
});
xAxis.render();
var yAxis = new Rickshaw.Graph.Axis.Y({
    graph: graph
});
yAxis.render();
var hoverDetail = new Rickshaw.Graph.HoverDetail( {
    graph: graph
} );
}
document.getElementById('post').onclick = function () {
  var ev = document.getElementById('algo')
  var selectedAlgo = ev.options[ev.selectedIndex].value
  console.log("SEL",selectedAlgo)
switch (parseInt(selectedAlgo)) {
  case 0: IQR();
    break;
  case 1: MMedian();
    break;
  case 2: MAvg();
    break;
  default:
    console.log("Wrong choice");

  }
}
//moving MAD
function IQR() {
  //iqr
    var e = document.getElementById("ip");
    var selectedIp = e.options[e.selectedIndex].text;

    //var param = document.getElementById('param').value;

    //var window_size = document.getElementById('window_size').value;
    //console.log("Slider",slider1._state.value[0])
    var filen = window.localStorage.getItem('current').split('.')

    var filename = filen[0]+".csv"
    var data = {
      ip : selectedIp,
      alpha : parseFloat(document.getElementById('textInput1').value),
      filename : filename
    }
      axios.post('/interq', data)
           .then(function(res) {
              var inlier = res.data.inliers;
              var outlier = res.data.outliers;
              draw(inlier, outlier)
           })
           .catch(function(err) {
             console.log(err);
           })
}

function MMedian() {
    var e = document.getElementById("ip");
    var selectedIp = e.options[e.selectedIndex].text;

    var filen = window.localStorage.getItem('current').split('.')

    var filename = filen[0]+".csv"
    var data = {
      ip : selectedIp,
      alpha : parseFloat(document.getElementById('textInput1').value),
      filename : filename,
      window_size : parseInt(document.getElementById('textInput2').value)
    }
      axios.post('/movmedian', data)
           .then(function(res) {
              var inlier = res.data.inliers;
              var outlier = res.data.outliers;
              draw(inlier, outlier)
           })
           .catch(function(err) {
             console.log(err);
           })
}


    //moving average
function MAvg() {
      var e = document.getElementById("ip");
      var selectedIp = e.options[e.selectedIndex].text;

      var param = document.getElementById('param').value;

      var window_size = document.getElementById('window_size').value;

      var filen = window.localStorage.getItem('current').split('.')

      var filename = filen[0]+".csv"
      var data = {
        ip : selectedIp,
        alpha : param,
        filename : filename,
        window_size : window_size
      }
        axios.post('/movmedian', data)
             .then(function(res) {
                var inlier = res.data.inliers;
                var outlier = res.data.outliers;
                draw(inlier, outlier)
             })
             .catch(function(err) {
               console.log(err);
             })
    }
