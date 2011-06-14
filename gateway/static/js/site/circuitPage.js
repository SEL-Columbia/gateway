/*  Javascript for the circuit overview page.
 *  deps on slickgrid and d3.js 
 */ 

function primaryLogGrid(options) { 

  var columns = [ 
    {id: "id", name:"Log id", width: 100, field: "id", sortable: true },  
    {id: "status", name:"Circuit Staus", field: "status", sortable: true, width: 100 },
    {id: "use_time", name:"Use time", field: "use_time", sortable: true, width: 100 },
    {id: "date", name:"Log Date", field: "date", sortable: true,width: 200 },
    {id: "watthours", name:"Watthours", field: "watthours", sortable: true, width: 100 },
    {id: "credit", name:"Credit", field: "credit", sortable: true, width: 100 }
  ]

  var logDataView = new Slick.Data.DataView();
  var logGrid = new Slick.Grid("#primary-logs",logDataView, columns, globalGridOptions)
  
  $.getJSON("/circuit/show_primary_logs/" + options.circuit, function(d) { 
    logDataView.beginUpdate();
    logDataView.setItems(d);
    logDataView.endUpdate();
    logGrid.invalidate();
  }); 
  return logGrid;

}

function loadGraph(options) { 
  
  $("#update-graph").click(function() { 
    $.ajax({ 
      url: '/circuit/show_graphing_logs/'  + options.circuit,
      data: $('form#date-ranges').serialize(),
      beforeSend: function() { 
        $('#graph').empty();
        $('#graph').append(
          $("<div />",{id: "ajax-loader"}).append($('<img>', {src: '/static/images/ajax-loader.gif'})));
      },
      method: 'GET',
      success: function(d) { 
        buildGraph(d);
      }
    })
  }); 

  $.ajax({ 
    url: '/circuit/show_graphing_logs/' + options.circuit,
    data: $('form#date-ranges').serialize(),
    method: 'GET',
    dataType: 'json',
    success: function(d) { 
      buildGraph(d);
    }
  })
  
  

  function buildGraph(d){
    $('#graph').empty();
    var w = $("#graph").width(),
        h = $("#graph").height(),
        top_margin = 20,
        left_margin = 70,
        right_margin = 20,
        bottom_margin = 100,
        dataY = d.values,
        dataX = d.dates,
        start = new Date($("#start").val()),
        end = new Date($("#end").val());



    /* 
     * FIX ME !!! we need to deal with time zones.
     */ 
      
    start.setHours(start.getHours() - 4); 
    end.setHours(end.getHours() - 4);



    var dateRange =  new Array();    
    dateRange.push((start.valueOf()/1000));

    var current = start;     
    while (current < end ) { 
      var date = current.getDate() + 1; 
      var current = new Date(current.getFullYear(), current.getMonth(), date, current.getHours());
      dateRange.push((current.valueOf() / 1000)); 
    }; 
        
    var y = d3.scale.linear().domain([0, d3.max(dataY)]).range([h - bottom_margin ,top_margin]);
    var x = d3.scale.linear().domain([(start.valueOf() / 1000),
                                      (end.valueOf() /1000)]).range([left_margin, w - right_margin]);

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
      var local_date = new Date(d * 1000);      
      return local_date.getDate() + " " +
        ("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(' ')[local_date.getMonth()]) + " " +
        local_date.getFullYear();
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
}

function loadBillingHistory(options) { 

  var columns = [ 
    {id: "id", name:"Database Id", width: 200, field: "id", sortable: true },
    {id: "credit", name:"Credit amount", width: 200, field: "credit", sortable: true },
    {id: "start", name:"Start of job", width: 200, field: "start", sortable: true },
    {id: "end", name:"End of job", width: 200, field: "end", sortable: true },
    {id: "state", name:"Job still running?", 
     width: 200, field: "state", sortable: true },
    {id: "token", name: "Token used", width: 200, field: "token", sortable: true}
  ]

  var logDataView = new Slick.Data.DataView();
  var logGrid = new Slick.Grid("#billing-history",logDataView, columns, globalGridOptions)
  
  $.getJSON("/circuit/get_payment_logs/" + options.circuit, function(d) { 
    logDataView.beginUpdate();
    logDataView.setItems(d.payments);
    logDataView.endUpdate();
    logGrid.invalidate();
  }); 
  return logGrid;

}


function loadPage(options) { 

  $("#logs").tabs();

  $("#date-ranges input").datepicker();

  
  
  loadBillingHistory(options)
  primaryLogGrid(options);
  loadGraph(options)
  
}
