var aqiGraphDetailInterval = setInterval(function (e) {
    if (typeof jQuery != 'function' || typeof Highcharts != 'object'){
        return false;
    }
    clearInterval(aqiGraphDetailInterval);
    $(document).ready(function () {
        // var data = randomData();
        // var range_map = $.range_map({
            // '0:1': 'red',
            // '2:4': 'yellow',
            // '5:7': 'black',
            // '8:9': 'blue',
            // '10:': 'purple'
        // })
        // $("#line1").sparkline(data, {
            // type: 'bar',
            // barColor: '#1ab394',
            // negBarColor: '#c6c6c6',
            // height: '35px',
            // barWidth: 8,
            // colorMap: eval($("#line1").attr('sparkColorMap'))
        // });
        
        
    });
}, 100);

// function randomData() {
    // var data = []
    // var i;
    // for (i = 0; i < 40; i++) {
        // data.push(Math.floor(Math.random() * 11));
    // } 
    // return data;
// }