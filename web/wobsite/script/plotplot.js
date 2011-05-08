
//The main data array for the plot
var plotData = [];
var graphHolder;
var plot;
var currentRanges = null; 	//holds the current ranges selection
var previousPoint = null;

var options = {
	series: {
		lines: { show: true },
		points: { show: true }
	},
	legend: { noColumns: 2 },
	xaxis: { tickDecimals: 0 },
	yaxis: { min: 0 },
	selection: { mode: "x" },
	grid: {	hoverable: true, 
			clickable: true}
};


function toolTip(event, pos, item){
	if (item) {
		if (previousPoint != item.dataIndex) {
			previousPoint = item.dataIndex;
			
			$("#tooltip").remove();
			var x = item.datapoint[0].toFixed(2),
				y = item.datapoint[1].toFixed(2);
			
			showTooltip(item.pageX, item.pageY - 30,
						item.series.label + " of " + y + " at " + x);
		}
	}
	else {
		$("#tooltip").remove();
		previousPoint = null;
	}
}

function showTooltip(x, y, contents) {
		$('<div id="tooltip">' + contents + '</div>').css( {
		position: 'absolute',
		display: 'none',
		top: y + 5,
		left: x + 5,
		border: '1px solid #fdd',
		padding: '2px',
		'background-color': '#fee',
		opacity: 0.80
	}).appendTo("body").fadeIn(200);
}
	

function addData(label, data, showPoints, showLines){
	var data = { 
				data : data,
				label : label,
				lines: {show: showLines},
				points: {show:showPoints}
				}; 
	
	plotData.push(data);
}

//takes a range and re-draws the plot with that range
function updatePlot(){
	if(currentRanges != null){
		plot = $.plot(graphHolder, plotData,
						$.extend(true, {}, options, {
							  xaxis: { min: currentRanges.xaxis.from, max: currentRanges.xaxis.to }
						  }));
	} else {
		plot = $.plot(graphHolder, plotData, options);
	}
}

//Resets the zoom and re-draws the plot
function zoomReset(){
	plot.clearSelection();
	currentRanges = null;
	plot = $.plot(graphHolder, plotData, options);
}


//Links two datasets based on timestamp and returns a dataset
function dataCorrelator(ds1, ds2){
	var t1 = 0;
	var t2 = 0;
	var result = [];
	
	while(t1 < ds1.length && t2 < ds2.length){
		if(t1 == ds1.length - 1 && ds1[t1][0] <= ds2[t2][0]){
			result.push([ds1[t1][1], ds2[t2][1]]);
			t2++;
		}else if(ds1[t1][0] <= ds2[t2][0] && ds2[t2][0] < ds1[t1 + 1][0]){
			result.push([ds1[t1][1], ds2[t2][1]]);
			t2++;
		} else{
			t1++;
		}
	}
	return result;
}

//Totes not working
function drawRegression(index){

	var data = plotData[index].data;
	var sumX = 0;
	var sumY = 0;
	var sumXY = 0;
	var sumXsqr = 0;
	var sumYsqr = 0;
	var n = data.length;
	
	for(var i=0;i < n; i++){
		var x = data[i][0];
		var y = data[i][1];
		
		sumX += x;
		sumY += y;
		sumXY += x*y;
		sumXsqr += x*x;
		sumYsqr += y*y;
	}
	
	slope = (n*sumXY - sumX*sumY) / (n*sumXsqr - sumX*sumX);
	intercept = (sumY - slope*sumX) / n;
	r = (n*sumXY - sumX*sumY) / Math.sqrt((n*sumXsqr - sumX*sumX)*(n*sumYsqr - sumY*sumY));
	
	var range_length = currentRanges.xaxis.to - currentRanges.xaxis.from;
	var x1 = currentRanges.xaxis.from + range_length*.2;
	var x2 = currentRanges.xaxis.from + range_length*.8;
	var reg_data =[[x1, x1* slope + intercept] , [x2, x2*slope + intercept]];
	
	//var regressionLabel = label + "Regression"
	
	plotData.push({ data : reg_data,lines: {show: true},
				points: {show:false}  });
	
	updatePlot();
}

	/*
function drawRegression(x1,x2,slope,intercept){

	var regressionData = {
						data: [[x1, slope*x1 + intercept],[x2, slope*x2 + intercept]],
						lines: {show:true},
						points: {show:false}
						};
	plotData.push(regressionData);
	
	$.plot(graphHolder, plotData,options);

} */





