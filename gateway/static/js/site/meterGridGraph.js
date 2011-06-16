
function loadPage(options) { 
  $("#grids").height($(window).height());
  
  var circuits = options.circuits;

  _.map(circuits, function(circuit) { 
    $("#grids").append($("<div />", {"id": circuit, "class": "circuit_grid"}));
    var graph = $("#" + circuit);
    
    $.ajax({ 
      url: '/circuit/show_graphing_logs/' + circuit,
      beforeSend: function() { 
        graph.append($('<img>', {"class": "ajax_loader", src: '/static/images/ajax-loader.gif'}));
      },
      success: function(d) { 
        buildGraph(circuit, d);
      }
    })
  }); 


  var offsetSeconds = new Date().getTimezoneOffset() * 60; 
  function buildDate(string) { 
    var year = parseInt(string.split("/")[2]); 
    var month = parseInt(string.split("/")[0]) - 1; 
    var date = +string.split("/")[1];
    var midnightLocal = new Date(year, month, date);
    var midnightLocalMilliseconds = midnightLocal.getTime();
    var midnightGMTSeconds = midnightLocalMilliseconds / 1000 - offsetSeconds;
    return midnightGMTSeconds;
  }


  function buildGraph(circuit, d){
    var graph = $("#" + circuit);

    graph.empty();
    var w = graph.width(),
        h = graph.height(),
        top_margin = 20,
        left_margin = 70,
        right_margin = 20,
        bottom_margin = 100,
        dataY = d.values,
        dataX = d.dates,
        startDateSeconds = buildDate($("#start").val()),
        endDateSeconds = buildDate($("#end").val());

    var dateRange =  new Array();
    var currentDateSeconds = startDateSeconds;
    while (currentDateSeconds <= endDateSeconds) {
      dateRange.push(currentDateSeconds);
      currentDateSeconds += 24 * 60 * 60;
    };     

    var y = d3.scale.linear().domain([0, d3.max(dataY)]).range([h - bottom_margin ,top_margin]);
    var x = d3.scale.linear().domain([startDateSeconds, endDateSeconds])
                             .range([left_margin, w - right_margin]);

    var vis = d3.select("#" + circuit)
      .append("svg:svg")
      .attr("width", w)
      .attr("height", h);

    console.log(vis);

    var g = vis.append("svg:g")

    g.selectAll(".xTicks")
      .data(dateRange)
      .enter().append("svg:line")
      .attr("x1", x)
      .attr("x2", x)
      .attr("y1", h - bottom_margin)
      .attr("y2", h - bottom_margin + 20)
      .attr("class","xTicks")
      .attr("stroke", "#808080")

    g.selectAll(".xGrid")
      .data(dateRange)
      .enter().append("svg:line")
      .attr("x1", x)
      .attr("stroke","#eee")
      .attr("x2", x)
      .attr("y1", top_margin)
      .attr("y2", h - bottom_margin)
      .attr("class","xGrid")

    g.selectAll(".yTicks")
      .data(y.ticks(10))
      .enter().append("svg:line")
      .attr("x1", left_margin)
      .attr("x2", left_margin -20)
      .attr("y1", function(d) { return y(d)})
      .attr("y2", function(d) { return y(d)})
      .attr("class","yTicks")
      .attr("stroke", "#808080")

    g.selectAll(".yGrid")
      .data(y.ticks(10))
      .enter().append("svg:line")
      .attr("stroke","#eee")
      .attr("x1", left_margin)
      .attr("x2", w - right_margin)
      .attr("y1", function(d) { return y(d)})
      .attr("y2", function(d) { return y(d)})
      .attr("class","yGrid")
     
    g.selectAll(".yLabel")
      .data(y.ticks(10))
      .enter().append("svg:text")
      .attr("class", "yLabel")
      .text(String)
      .attr("x", left_margin-20)
      .attr("y", function(d) { return y(d)})
      .attr("text-anchor", "end")
      .attr("dy", ".25em")
      .attr("dx","-0.5em")


    function prettyDateString(d){
      var UTCDateTick = new Date(d * 1000);
      // getUTC methods are necessary to keep date from being interpreted locally  
      return UTCDateTick.getUTCDate() + " " +
       ("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(' ')[UTCDateTick.getUTCMonth()])
       + " " + UTCDateTick.getUTCFullYear();
    }
    
    g.selectAll(".xLabel")
      .data(dateRange)
      .enter().append("svg:text")
      .attr("class", "xLabel")
      .text(prettyDateString)
      .attr("x", function(d) { return x(d) ;})    
      .attr("y", h - bottom_margin + 20)
      .attr("dx","-0.5em")
      .attr("dy","0.25em")
      .attr("transform", function(d) { 
        return "rotate(-60, "+ x(d) +", " + (h - bottom_margin + 20) +" )"; 
      })
      .attr("text-anchor", "end")
    

    var dots = g.selectAll("circle")
      .data(dataX)      
      .enter().append("svg:circle")
      .attr("cx", function(d,i) {  
        return x(dataX[i])
      })
      .attr("cy", function(d, i) { return y(dataY[i])})
      .attr("r", 2)
      .attr("fill", "#000");



  }
};
