$(function() { 

  $.getJSON('/circuit/show_circuit_logs/13')
      .done(buildGraph);
  
  $('#update-graph').click(function() {     
    $.getJSON('/circuit/show_circuit_logs/13',$('form#date-ranges').serialize()).done(buildGraph);
  })
  var w = 800;
  var h = 400;
  var margin = 50;

function buildGraph(d){

  $('#graph').empty();
  var dataX = d.dates;
  var dataY = d.watthours; 
  var y = d3.scale.linear().domain([0, d3.max(dataY)]).range([margin, h - margin]);
  var x = d3.scale.linear().domain([d3.min(dataX), d3.max(dataX)]).range([margin, w - margin]);

  var vis = d3.select("#graph")
    .append("svg:svg")
    .attr("width", w)
    .attr("height", h);
 
  var g = vis.append("svg:g");

  var dot = g.selectAll("circle")
    .data(dataX)
    .enter().append("svg:circle")
    .attr("cx", function(d,i) {  
      return x(dataX[i])
    })
    .attr("cy", function(d, i) { 
      return y(dataY[i])
    })
    .attr("r", 2)
    .attr("fill", "808080");
}
})
