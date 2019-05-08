
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
	var inc_label = [];
	var datapoints = [];
	var num = 0;
	final_array.forEach(e => {
	  datapoints.push({'x' : e[0],'y' : e[1], 'r' : num+=1});
	  
		})
	console.log(datapoints)

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
				// labels:[y_res,896,768,640,512,384,256,128],
				datasets: [{
					label: 'Common Scanpath',
					data: 
					datapoints
				,
				backgroundColor: dynamicColors(),
				hoverBackgroundColor:dynamicColors(),
				// useRandomColors: true,
				pointBackgroundColor: dynamicColors(),
				pointBorderColor: dynamicColors(),
				borderColor: dynamicColors(),
				pointRadius: 20,
				pointHoverRadius: 20,
				fill: false,
				tension: 0,
				showLine: true
			}],
			options: {
				responsive: true,
				scales: {
					yAxes: [{
						display:true,
						type: 'number',
						position: 'left',
						ticks: {
							min: y_res,
							max: 0,
							callback: function (value, index, values) {
								 return Number(value.toString());//pass tick values as a string into Number function
							 }
						},
						afterBuildTicks: function (chartObj) { //Build ticks labelling as per your need
							chartObj.ticks = [y_res,896,768,640,512,384,256,128];
							
						},
						gridLines: {
							display: false,
							drawBorder: false
						}
					}],
					xAxes: [{
						position: 'bottom',
						ticks: {
							min: 0, // Controls where axis starts
							max: x_res,// Controls where axis finishes
							suggestedMax: x_res+20,
							callback: function (value, index, values) {
								 return Number(value.toString());//pass tick values as a string into Number function
							 }
						},
						afterBuildTicks: function (chartObj) { //Build ticks labelling as per your need
							chartObj.ticks = [x_res,896,768,640,512,384,256,128];
						 }
						 // ,
						// gridLines: {
						// 	display: false,
						// 	lineWidth: 2 // Width of bottom line
						// }
				 
					}]
				}

			}
			
		}	
	});
// }

}

