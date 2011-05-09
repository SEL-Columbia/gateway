
function loadPage(data) { 

  var gridOptions = {
    forceFitColumns: true,
    autoHeight: true,
    enableCellNavigation: true,
    enableColumnReorder: true
  };


  function MeterLinkFormatter(row, cell, value, columnDef, data) { 
    return "<a href=\"/meter/index/" + data.id + "\">" + value + "</a>";
  }; 
  
  var columns = [ 
    {id: "name", name: "Meter", field: "name", formatter: MeterLinkFormatter, sortable: true},
    {id: "location", name: "Location", field: "location"},
    {id: "number_of_circuits", name: "# Circuits", field: "number_of_circuits"},
    {id: "pv ", name: "PV (kw)", field: "pv"},
    {id: "battery", name: "Battery (kWh)", field: "battery", sortable: true},
    {id: "phone", name: "Phone Number", field: "phone"}
  ]

  var dataView = new Slick.Data.DataView();
  dataView.beginUpdate();
  dataView.setItems(data);
  dataView.endUpdate();

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



  $("#meterGrid").show();
  
}
