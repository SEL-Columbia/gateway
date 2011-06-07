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

  $.ajax({ 
    url: '/circuit/show_graphing_logs/' + options.circuit,
    method: 'GET',
    dataType: 'json',
    beforeSend: function() {       
    }, 
    complete: function() { 
      $("#graph").css("background","#eee");
    },
    success: function(d) { 
      buildGraph(d);
    }
  })
  
  
  $('#update-graph').click(function() {     
    $.getJSON('/circuit/show_graphing_logs/' + options.circuit, 
              $('form#date-ranges').serialize()).done(buildGraph);
  })


  var w = $("#graph").width();
  var h = $("#graph").height();
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
  

  loadBillingHistory(options)
  primaryLogGrid(options);
  loadGraph(options)
  
}
