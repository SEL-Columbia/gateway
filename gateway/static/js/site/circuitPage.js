/*  Javascript for the circuit overview page.
 *  deps on slickgrid and d3.js 
 */ 

function primaryLogGrid(options) { 

  var columns = [ 
    {id: "id", name:"Log id", width: 100, field: "id", sortable: true },  
    {id: "status", name:"Circuit Staus", field: "status", sortable: true, width: 100 },
    {id: "use_time", name:"Use time", field: "use_time", sortable: true, width: 100 },
    {id: "gateway_date", name:"Gateway Receive Time", field: "gateway_date", sortable: true,width: 200 },
    {id: "meter_date", name:"Meter Timestamp", field: "meter_date", sortable: true,width: 200 },
    {id: "time_difference", name:"Time Difference", field: "time_difference", sortable: true,width: 200 },
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

  logGrid.onSort.subscribe(function(e, args) { 
    sortdir = args.sortAsc ? 1 : -1;
    sortcol = args.sortCol.field;
   logDataView.sort(comparer, args.sortAsc);
  });

  logDataView.onRowsChanged.subscribe(function(e,args) {
    logGrid.invalidateRows(args.rows);
    logGrid.render();
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
        buildGraph({ 
          selector: "#graph",
          data: d
        });
      }
    })

  }); 

  $.ajax({ 
    url: '/circuit/show_graphing_logs/' + options.circuit,
    data: $('form#date-ranges').serialize(),
    method: 'GET',
    dataType: 'json',
    success: function(d) {       
      try { 
        buildGraph({ 
          selector: "#graph",
          data: d,
        });
      } catch (error) { 
        console.log(error);
      }
    }
  })

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
  var logGrid = new Slick.Grid("#billing-history",logDataView, columns,
                               globalGridOptions)
  
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
