  var sortdir, sortcol;

  function comparer(a, b) { 
    var x = a[sortcol], y = b[sortcol];
/*--
x     y     result
10    1     1
1     10    -1
1     1     0
''    0     -1
0     ''    1
  --*/
    if(x===null) {return -1}
    if(y===null) {return 1}
    return (x === y ? 0 : (x > y ? 1 : -1));
  }; 


  var globalGridOptions = {
    forceFitColumns: false,
    autoHeight: true,
    enableCellNavigation: true,
    enableColumnReorder: true
  };


/*
 *offsetSeconds is opposite sign of usual offset
 * i.e. EDT(GMT-4) -> offsetSeconds = +14400
 */
 

function buildDate(string) { 
  var offsetSeconds = new Date().getTimezoneOffset() * 60; 
  var year = parseInt(string.split("/")[2]); 
  var month = parseInt(string.split("/")[0]) - 1; 
  var date = +string.split("/")[1];
  var midnightLocal = new Date(year, month, date);
  var midnightLocalMilliseconds = midnightLocal.getTime();
  var midnightGMTSeconds = midnightLocalMilliseconds / 1000 - offsetSeconds;
  return midnightGMTSeconds;
}

function loadCircuitData(options) { 
  var div = $(options.selector);
  $.ajax({ 
    url: '/circuit/show_graphing_logs/'  + options.circuit,
    data: $('form#date-ranges').serialize(),
    beforeSend: function() { 
      div.empty();
      div.append(
        $("<div />",{id: "ajax-loader"}).append($('<img>', {src: '/static/images/ajax-loader.gif'})));
    },
    method: 'GET',
    success: function(d) { 
      buildGraph({ 
        selector: options.selector,
        data: d
      });
    }
  })
};

function graphPCULogs(options) { 
  var url = options.url;
  var selector = options.selector;
  var form = options.form;
  $.ajax({ 
    url: url,
    data: form.serialize(),
    success: function(d) { 
      buildGraph({
        selector: options.selector,
        data: d
      })
    },
    error: function(e) { 
      console.log(e);
    }
  })
}



function updateGraph(options) { 
  var graph = $(options.selector);
  $(options.button).click(function() { 
    $.ajax({ 
      url: '/circuit/show_graphing_logs/'  + options.circuit,
      data: options.form.serialize(),
      beforeSend: function() { 
        graph.empty();
        graph.append(
          $("<div />",{id: "ajax-loader"}).append($('<img>', {src: '/static/images/ajax-loader.gif'})));
      },
      method: 'GET',
      success: function(d) { 
        buildGraph({ 
          selector: options.selector,
          data: d
        });
      }
    })
  }); 


}; 


function buildGraph(options){
  /* Function to build a graph with d3.js
   * Args 
   *  selector:
   *  data: 
   */ 
  d = options.data,
  div = $(options.selector);
  $(options.selector).empty();
  

  var w = div.width(),
      h = div.height(),
      top_margin = 20,
      left_margin = 70,
      right_margin = 20,
      bottom_margin = 100,
      dataY = d.values,
      dataX = d.dates;


  var startDateSeconds = buildDate($("#start").val());
  var endDateSeconds = buildDate($("#end").val());



  var dateRange =  new Array();
  var currentDateSeconds = startDateSeconds;
  while (currentDateSeconds <= endDateSeconds) {
    dateRange.push(currentDateSeconds);
    currentDateSeconds += 24 * 60 * 60;
  };     
 


  var y = d3.scale.linear().domain([0, d3.max(dataY)]).range([h - bottom_margin ,top_margin]);
  var x = d3.scale.linear().domain([startDateSeconds, endDateSeconds])
    .range([left_margin, w - right_margin]);




  var vis = d3.select("#graph")
    .append("svg:svg")
    .attr("width", w)
    .attr("height", h);
  
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
};

