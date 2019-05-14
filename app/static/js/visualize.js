
window.onload=function(){
	var x_res_element = document.getElementsByClassName("x_res");
	var x_res = parseInt(x_res_element[0].value);
	var x_axis = x_res/8;
	console.log(x_axis);

	var y_res_element = document.getElementsByClassName("y_res");
	var y_res = parseInt(y_res_element[0].value);
	var y_axis = x_res/8;
	console.log(y_axis);
	console.log(y_axis);

	var sequences_element = document.getElementsByClassName("sequences");
	var sequence = sequences_element[0].value;
	var arr_seq = sequence.replace(/[\[\]']+/g,'');
	var array_seq = arr_seq.split(',').map(function(item) {
		return parseInt(item, 10);
	});

	var final_array = [];
	var i;
	var num = 0;
	var iter = 0;

	for (i=0; i<(array_seq.length/2); i++){
	  final_array.push({'x':array_seq[i],'y':array_seq[i+1],'r':num+=1});
	  i++;
	} 

	console.log(final_array)

	var dynamicColors = function() {
		var r = Math.floor(Math.random() * 255);
		var g = Math.floor(Math.random() * 255);
		var b = Math.floor(Math.random() * 255);
		return "rgb(" + r + "," + g + "," + b + ")";
	}

	var ctx = document.getElementById("myChart");
	ctx.height = y_res;
	ctx.width = x_res;


		var bubbleChart = new Chart(ctx, {
			type: 'scatter',
			data: {
				datasets: [{
					label: 'Common Scanpath',
					data: 
					final_array
				,
				backgroundColor: dynamicColors(),
				hoverBackgroundColor:dynamicColors(),
				pointBackgroundColor: dynamicColors(),
				pointBorderColor: dynamicColors(),
				borderColor: dynamicColors(),
				pointRadius: 20,
				pointHoverRadius: 20,
				fill: false,
				tension: 0,
				showLine: true
			}],
		},
			options: {

				responsive: true,
				scales: {
					yAxes: [{
						display:true,
						type: 'linear',
						position: 'left',
						ticks: {
							min: 0,
							max: y_res,
							stepSize: x_axis
							
						},
					}],
					xAxes: [{
						position: 'bottom',
						ticks: {
							min: 0, // Controls where axis starts
							max: x_res,// Controls where axis finishes
							stepSize: y_axis
							
						},
					}]
				}

			}
	});
// }

}

