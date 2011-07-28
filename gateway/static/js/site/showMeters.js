
function loadPage(data) { 

  var gridOptions = {
    forceFitColumns: false,
    autoHeight: true,
    enableCellNavigation: true,
    enableColumnReorder: true
  };


  function MeterLinkFormatter(row, cell, value, columnDef, data) { 
    return "<a href=\"/meter/index/" + data.id + "\">" + value + "</a>";
  }; 
  
  var columns = [ 
    {id: "name", name: "Meter", field: "name", formatter: MeterLinkFormatter, sortable: true, width: 100},
    {id: "last_message ", name: "Last Message", field: "last_message", sortable: true, width: 200},
    {id: "location", name: "Location", field: "location", sortable: true, width: 100},
    {id: "number_of_circuits", name: "# Circuits", field: "number_of_circuits", sortable: true, width: 100},
    {id: "pv ", name: "PV (kw)", field: "pv", sortable: true, width: 100},
    {id: "battery", name: "Battery (kWh)", field: "battery", sortable: true, width: 100},
    {id: "phone", name: "Phone Number", field: "phone", sortable: true, width: 100},
    {id: "uptime", name: "Meter Uptime (7 Days)", field: "uptime", sortable: true, width: 200}
  ]

  var dataView = new Slick.Data.DataView();

  var grid = new Slick.Grid("#meterGrid", dataView, columns, gridOptions);
  
  grid.onSort.subscribe(function(e, args) { 
    sortdir = args.sortAsc ? 1 : -1;
    sortcol = args.sortCol.field;
    dataView.sort(comparer, args.sortAsc);
  });

  dataView.onRowsChanged.subscribe(function(e,args) {
    grid.invalidateRows(args.rows);
    grid.render();
  });


  $.getJSON("/manage/show_meters_json", function(d) { 
    dataView.beginUpdate();
    dataView.setItems(d);
    dataView.endUpdate();
    grid.invalidate();
  })



  $("#meterGrid").show();
  
}
