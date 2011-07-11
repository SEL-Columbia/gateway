$(function(){ 
  var columns = [
    {id: "id", name: "Alert id", field: "id", sortable:true},
    {id: "type", name: "Alert type", field: "type", sortable:true},
    {id: "date", name: "Date of alert", field: "date", sortable:true},
    {id: "meter", name: "Meter associated with alert", field: "meter", sortable:true},
    {id: "circuit", name: "Circuit associated with alert", field: "circuit", sortable:true}
  ]

  var alertDataView = new Slick.Data.DataView();
  var alertGrid = new Slick.Grid("#alert-grid", alertDataView, columns, globalGridOptions);

  $.getJSON("/alerts/all", function(data) { 
    alertDataView.beginUpdate();
    alertDataView.setItems(data);
    alertDataView.endUpdate();
    alertGrid.invalidate();
  }); 

  
  alertGrid.onSort.subscribe(function(e, args) { 
    sortdir = args.sortAsc ? 1 : -1;
    sortcol = args.sortCol.field;
    alertDataView.sort(comparer, args.sortAsc);
  });

  alertDataView.onRowsChanged.subscribe(function(e,args) {
    alertGrid.invalidateRows(args.rows);
    alertGrid.render();
  });

})
