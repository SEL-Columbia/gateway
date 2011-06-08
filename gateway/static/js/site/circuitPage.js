/*  Javascript for the circuit overview page.
 *  deps on slickgrid and d3.js 
 */ 

function primaryLogGrid(options) { 

  var columns = [ 
    {id: "id", name:"Database Id", width: 200, field: "id", sortable: true },
    
    {id: "str", name:"Log String", width: 600, field: "str", sortable: true }
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
    method: 'GET',
    dataType: 'json',
    beforeSend: function() {       
    }, 
    complete: function() { 
    },
    success: function(d) { 
      buildGraph(d);
    }
  })
  
  

  function buildGraph(d){

    var w = $("#graph").width();
    var h = $("#graph").height();
    var margin = 50;



    $('#graph').empty();
    var dataX = d.dates;
    var dataY = d.values; 
    var y = d3.scale.linear().domain([0, d3.max(dataY)]).range([h - margin ,margin]);
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
      .attr("cy", function(d, i) { return y(dataY[i])})
      .attr("r", 3)
      .attr("fill", "808080");


    g.selectAll(".xTicks")
      .data(x.ticks(10))
      .enter().append("svg:line")
      .attr("x1", x)
      .attr("x2", x)
      .attr("y1", h)
      .attr("y2", h - 10)
      .attr("class","xTicks")
      .attr("stroke", "#808080")

    g.selectAll(".yTicks")
      .data(y.ticks(10))
      .enter().append("svg:line")
      .attr("x1", 25)
      .attr("x2", 40)
      .attr("y1", function(d) { return y(d)})
      .attr("y2", function(d) { return y(d)})
      .attr("class","yTicks")
      .attr("stroke", "#808080")

    
    g.selectAll(".yLabel")
      .data(y.ticks(10))
      .enter().append("svg:text")
      .attr("class", "yLabel")
      .text(String)
      .attr("x", 0)
      .attr("y", function(d) { return y(d)})
      .attr("text-anchor", "right")
      .attr("dy", 4)

  }
}

function loadBillingHistory(options) { 

  var columns = [ 
    {id: "id", name:"Database Id", width: 200, field: "id", sortable: true },
    {id: "credit", name:"Credit amount", width: 200, field: "credit", sortable: true },
    {id: "date", name:"Date", width: 200, field: "date", sortable: true },
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
