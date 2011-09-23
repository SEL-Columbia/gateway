function loadGrid() { 

  var columns = [
    {id: "meter_name", name: "Meter", field: "meter_name", sortable:true},
    {id: "start_gateway_time", name: "Start Gap Time (Gateway)", field: "start_gateway_time", width:180, sortable:true},
    {id: "end_gateway_time", name: "End Gap Time (Gateway)", field: "end_gateway_time", width:180, sortable:true},
    {id: "start_meter_time", name: "Start Gap Time (Meter)", field: "start_meter_time", width:180, sortable:true},
    {id: "end_meter_time", name: "End Gap Time (Meter)", field: "end_meter_time", width:180, sortable:true},
    {id: "gap_seconds", name: "Gap Size (seconds)", field: "gap_seconds", width:180, sortable:true},
    {id: "end_circuit", name: "Circuit ID", field: "end_circuit", sortable:true}
  ]

  var gapDataView = new Slick.Data.DataView();
  var gapGrid = new Slick.Grid("#gap-grid", gapDataView, columns, globalGridOptions);

  var formData = $("#gap_form").serialize();

  $.post("/manage/show_gaps_json", formData, function(data) { 
    gapDataView.beginUpdate();
    gapDataView.setItems(data);
    gapDataView.endUpdate();
    gapGrid.invalidate();
  }, "json"); 


  /*
    $.getJSON("/manage/show_gaps_json", function(data) { 
    gapDataView.beginUpdate();
    gapDataView.setItems(data);
    gapDataView.endUpdate();
    gapGrid.invalidate();
  });  
  */

  
  gapGrid.onSort.subscribe(function(e, args) { 
    sortdir = args.sortAsc ? 1 : -1;
    sortcol = args.sortCol.field;
    gapDataView.sort(comparer, args.sortAsc);
  });

  gapDataView.onRowsChanged.subscribe(function(e,args) {
    gapGrid.invalidateRows(args.rows);
    gapGrid.render();
  });

  $("#gap-grid").show();

}
