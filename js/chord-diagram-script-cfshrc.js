////////////////////////////////////////////////////////////
//////////////////////// Set-Up ////////////////////////////
////////////////////////////////////////////////////////////

var margin = {left:20, top:20, right:20, bottom:20},
	width = Math.min(window.innerWidth, 700) - margin.left - margin.right,
    height = Math.min(window.innerWidth, 700) - margin.top - margin.bottom,
    innerRadius = Math.min(width, height) * .39,
    outerRadius = innerRadius * 1.1;
	
var Names = ["CFSHRC","Coalition*","@drbohannon","@drccedillo","fancher","Feminist*","Women*","#C17","@karriemariesoto","#medrhet","#thefeministsarecoming","@jennfishperson","Intersection*","@ruthieoo","@mariatnovotny","@rachelbigeyes"],
	colors = ["#8B161C", "#083E77", "#342350", "#567235", "#301E1E", "#feff00","#82168b","#67a8b5","#DF7C00","#7a7a7a","#00ff34","#ffba63","#63f3ff","#f00511","#ff878d","#b9a000","#5bdea6","#fbb3f3","#849200","#f2df5c","#e26c2c","#f359ff"],
	opacityDefault = 0.8;

// rsa16 keyword cross-mentions
var matrix = [
	[0,20,5,0,5,22,10,0,2,1,47,5,2,1,0,0],	// cfshrc
	[20,0,0,0,0,11,0,0,0,0,14,0,0,0,0,0],	// coalition
	[5,0,0,0,2,0,0,0,3,0,3,2,0,0,0,0],	// drbohannon
	[0,0,0,0,0,0,4,10,0,0,0,0,0,0,0,0],	// drccedillo
	[5,0,2,0,0,3,0,0,2,0,2,2,0,0,0,0],	// fancher
	[22,11,0,0,3,0,0,0,3,14,65,7,19,4,9,15],	// fem
	[10,0,0,4,0,0,0,0,0,0,0,0,0,1,6,5],	// women
	[0,0,0,10,0,0,0,0,7,0,0,0,0,0,0,0],	// c17
	[2,0,3,0,2,3,0,0,7,0,0,0,0,0,0,0], // karriemariesoto
	[1,0,0,0,0,14,0,0,0,0,0,0,10,0,17,0], // medrhet
	[47,14,3,0,0,65,0,0,0,0,0,0,3,0,0,0], // thefeministsarecoming
	[5,0,2,0,2,7,0,0,0,0,0,0,0,0,0,0], // jennfishperson
	[2,0,0,0,0,19,0,0,0,10,3,0,0,12,1,0], // intersection
	[1,0,0,0,0,4,1,0,0,0,0,0,12,0,0,0], // @ruthieoo
	[0,0,0,0,0,9,6,0,0,17,0,0,1,0,0,0], // @mariatnovotny
	[0,0,0,0,0,15,5,0,0,0,0,0,0,0,0,0], // @rachelbigeyes
];

////////////////////////////////////////////////////////////
/////////// Create scale and layout functions //////////////
////////////////////////////////////////////////////////////

var colors = d3.scale.ordinal()
    .domain(d3.range(Names.length))
	.range(colors);

//A "custom" d3 chord function that automatically sorts the order of the chords in such a manner to reduce overlap	
var chord = customChordLayout()
    .padding(.05)
    .sortChords(d3.descending) //which chord should be shown on top when chords cross. Now the biggest chord is at the bottom
	.matrix(matrix);
		
var arc = d3.svg.arc()
    .innerRadius(innerRadius*1.01)
    .outerRadius(outerRadius);

var path = d3.svg.chord()
	.radius(innerRadius);
	
////////////////////////////////////////////////////////////
////////////////////// Create SVG //////////////////////////
////////////////////////////////////////////////////////////
	
var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
	.append("g")
    .attr("transform", "translate(" + (width/2 + margin.left) + "," + (height/2 + margin.top) + ")");

////////////////////////////////////////////////////////////
/////////////// Create the gradient fills //////////////////
////////////////////////////////////////////////////////////

//Function to create the id for each chord gradient
function getGradID(d){ return "linkGrad-" + d.source.index + "-" + d.target.index; }

//Create the gradients definitions for each chord
var grads = svg.append("defs").selectAll("linearGradient")
	.data(chord.chords())
   .enter().append("linearGradient")
	.attr("id", getGradID)
	.attr("gradientUnits", "userSpaceOnUse")
	.attr("x1", function(d,i) { return innerRadius * Math.cos((d.source.endAngle-d.source.startAngle)/2 + d.source.startAngle - Math.PI/2); })
	.attr("y1", function(d,i) { return innerRadius * Math.sin((d.source.endAngle-d.source.startAngle)/2 + d.source.startAngle - Math.PI/2); })
	.attr("x2", function(d,i) { return innerRadius * Math.cos((d.target.endAngle-d.target.startAngle)/2 + d.target.startAngle - Math.PI/2); })
	.attr("y2", function(d,i) { return innerRadius * Math.sin((d.target.endAngle-d.target.startAngle)/2 + d.target.startAngle - Math.PI/2); })

//Set the starting color (at 0%)
grads.append("stop")
	.attr("offset", "0%")
	.attr("stop-color", function(d){ return colors(d.source.index); });

//Set the ending color (at 100%)
grads.append("stop")
	.attr("offset", "100%")
	.attr("stop-color", function(d){ return colors(d.target.index); });
		
////////////////////////////////////////////////////////////
////////////////// Draw outer Arcs /////////////////////////
////////////////////////////////////////////////////////////

var outerArcs = svg.selectAll("g.group")
	.data(chord.groups)
	.enter().append("g")
	.attr("class", "group")
	.on("mouseover", fade(.1))
	.on("mouseout", fade(opacityDefault));

outerArcs.append("path")
	.style("fill", function(d) { return colors(d.index); })
	.attr("d", arc)
	.each(function(d,i) {
		//Search pattern for everything between the start and the first capital L
		var firstArcSection = /(^.+?)L/; 	

		//Grab everything up to the first Line statement
		var newArc = firstArcSection.exec( d3.select(this).attr("d") )[1];
		//Replace all the comma's so that IE can handle it
		newArc = newArc.replace(/,/g , " ");
		
		//If the end angle lies beyond a quarter of a circle (90 degrees or pi/2) 
		//flip the end and start position
		if (d.endAngle > 90*Math.PI/180 & d.startAngle < 270*Math.PI/180) {
			var startLoc 	= /M(.*?)A/,		//Everything between the first capital M and first capital A
				middleLoc 	= /A(.*?)0 0 1/,	//Everything between the first capital A and 0 0 1
				endLoc 		= /0 0 1 (.*?)$/;	//Everything between the first 0 0 1 and the end of the string (denoted by $)
			//Flip the direction of the arc by switching the start en end point (and sweep flag)
			//of those elements that are below the horizontal line
			var newStart = endLoc.exec( newArc )[1];
			var newEnd = startLoc.exec( newArc )[1];
			var middleSec = middleLoc.exec( newArc )[1];
			
			//Build up the new arc notation, set the sweep-flag to 0
			newArc = "M" + newStart + "A" + middleSec + "0 0 0 " + newEnd;
		}//if
		
		//Create a new invisible arc that the text can flow along
		svg.append("path")
			.attr("class", "hiddenArcs")
			.attr("id", "arc"+i)
			.attr("d", newArc)
			.style("fill", "none");
	});

////////////////////////////////////////////////////////////
////////////////// Append Names ////////////////////////////
////////////////////////////////////////////////////////////

//Append the label names on the outside
outerArcs.append("text")
	.attr("class", "titles")
	.attr("dy", function(d,i) { return (d.endAngle > 90*Math.PI/180 & d.startAngle < 270*Math.PI/180 ? 25 : -16); })
   .append("textPath")
   	.attr("class", "textpath-titles")
	.attr("startOffset","50%")
	.style("text-anchor","middle")
	.attr("xlink:href",function(d,i){return "#arc"+i;})
	.text(function(d,i){ return Names[i]; });
	
////////////////////////////////////////////////////////////
////////////////// Draw inner chords ///////////////////////
////////////////////////////////////////////////////////////
  
svg.selectAll("path.chord")
	.data(chord.chords)
	.enter().append("path")
	.attr("class", "chord")
	.style("fill", function(d){ return "url(#" + getGradID(d) + ")"; })
	.style("opacity", opacityDefault)
	.attr("d", path)
	.on("mouseover", mouseoverChord)
	.on("mouseout", mouseoutChord);

////////////////////////////////////////////////////////////
////////////////// Extra Functions /////////////////////////
////////////////////////////////////////////////////////////

//Returns an event handler for fading a given chord group.
function fade(opacity) {
  return function(d,i) {
    svg.selectAll("path.chord")
        .filter(function(d) { return d.source.index !== i && d.target.index !== i; })
		.transition()
        .style("opacity", opacity);
  };
}//fade

//Highlight hovered over chord
function mouseoverChord(d,i) {
  
	//Decrease opacity to all
	svg.selectAll("path.chord")
		.transition()
		.style("opacity", 0.1);
	//Show hovered over chord with full opacity
	d3.select(this)
		.transition()
        .style("opacity", 1);
  
	//Define and show the tooltip over the mouse location
	$(this).popover({
		placement: 'auto top',
		container: 'body',
		mouseOffset: 10,
		followMouse: true,
		trigger: 'hover',
		html : true,
		content: function() { 
			return "<p style='font-size: 11px; text-align: center;'><span style='font-weight:900'>" + Names[d.source.index] + 
				   "</span> and <span style='font-weight:900'>" + Names[d.target.index] + 
				   "</span> appeared together in <span style='font-weight:900'>" + d.source.value + "</span> tweets </p>"; }
	});
	$(this).popover('show');
}//mouseoverChord

//Bring all chords back to default opacity
function mouseoutChord(d) {
	//Hide the tooltip
	$('.popover').each(function() {
		$(this).remove();
	}); 
	//Set opacity back to default for all
	svg.selectAll("path.chord")
		.transition()
		.style("opacity", opacityDefault);
}//function mouseoutChord