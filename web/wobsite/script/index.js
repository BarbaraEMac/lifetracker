
var sleep_data = [[ 1,8], [2,7], [3,7],	[4,10], [5,7],[6,5],[7,5],[8,8],[9,3],[10,7],[11,5],[12,8],[13,8],[14,9],[15,10],[16,9],[17,9]];

var mood_data =[[1,1],[1.3,6],[1.6,3],[1.9,8],[2.2,9],[2.5,9],[2.8,7],[3.1,7],[3.4,3],[3.7,5],[4.0,10],[4.3,9],[4.6,1],[4.9,3],[5.2,2],[5.5,6],[5.8,3],[6.1,2]];



$(document).ready(function(){
	graphHolder = $("#placeholder");
	
	addData("Sleep" , sleep_data);
	addData("Mood", mood_data);
	
	//addData("Sleep vs. Mood", dataCorrelator(sleep_data, mood_data), true, false);
	
	updatePlot();
	
	graphHolder.bind("plotselected", function (event, ranges) {
		currentRanges = ranges;
		$("#selection").text(ranges.xaxis.from.toFixed(1) + " to " + ranges.xaxis.to.toFixed(1));
	});
	
	graphHolder.bind("plothover", function (event, pos, item) { toolTip(event,pos,item); });	


	
	$("#zoom").click(function(){
		updatePlot();
		
	});
	
	$("#clearSelection").click(function () {
		zoomReset();
		$("#selection").text("nothing!");
	});
	

});
