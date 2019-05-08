window.onload=function(){
    var x_res_element = document.getElementsByClassName("x_res");
    var x_res = parseInt(x_res_element[0].value);
    console.log(typeof(x_res));
    var y_res_element = document.getElementsByClassName("y_res");
    var y_res = parseInt(y_res_element[0].value);
    console.log(y_res);
    var sequences_element = document.getElementsByClassName("sequences");
    var sequence = sequences_element[0].value;
    var arr_seq = sequence.replace(/[\[\]']+/g,'');

    var array_seq = arr_seq.split(',').map(function(item) {
        return parseInt(item, 10);
    });

    var final_array = [];
    var i;
    for (i=0; i<(array_seq.length/2); i++){
      final_array.push([array_seq[i],array_seq[i+1]]);
    } 
    // var i = 0;
    // var len = cars.length;
    // for (; i < len; ) {
    //   text += cars[i] + "<br>";
    //   i++;
    // } 

    for(var j = 0; j < ((final_array.length*2)-1); j++){
        console.log(final_array[j]);
    Chart.defaults.global.defaultColor = '#000000'; 


     let massPopChart = new Chart(myChart, {
                type: 'bubble',
                    data: {
                        datasets: [{label: 'Data Set', data: final_array}],
                    },
                    options: {
                        scales: {
                            yAxes: [{
                                ticks: {
                                    max: 200,
                                    min: 0,
                                    beginAtZero:true
                                },
                            }]

                        }
                    }       
            });