var grid;
function loadGrid(options) { 
//  $("#grid").css("height",400);

  var gridOptions = {
    autoHeight: true,
    enableCellNavigation: true,
    enableColumnReorder: true
  };

  function CircuitLinkFormatter(row, cell, value, columnDef, data) { 
    return "<a href=\"/circuit/index/" + data.id + "\">" + value + "</a>";
  }; 
  
  var columns = [ 
    {id: "account", name: "Account", 
     formatter: CircuitLinkFormatter,
     field: "account", sortable:true},
    {id: "id", name: "Id", 
     field: "id", sortable:true}, 
    {id: "ip_address", 
     width: 100,
     name: "Ip Address", 
     field: "ipaddress", 
     sortable:true},
    {id: "status", name: "Status", 
     formatter:BoolCellFormatter,
     field: "status", sortable: true },
    {id: "credit", name: "Credit", field: "credit", sortable:true}
  ]; 

  var dataView = new Slick.Data.DataView();
  
  grid = new Slick.Grid("#grid", dataView, columns, gridOptions);

  $.getJSON("/meter/circuits/" + options.meter, function(data){ 
    dataView.beginUpdate();
    dataView.setItems(data);
    dataView.endUpdate();
    grid.invalidate();
    grid.render();

  }); 
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

  grid.onSort.subscribe(function(e, args) { 
    sortdir = args.sortAsc ? 1 : -1;
    sortcol = args.sortCol.field;

    dataView.sort(comparer, args.sortAsc);
  });

  dataView.onRowsChanged.subscribe(function(e,args) {
    grid.invalidateRows(args.rows);
    grid.render();
  });

  $("#grid").show();
  return grid; 
}

function loadMap(div) {
  var map = new OpenLayers.Map('map', {
      allOverlays: true,
      controls: []
    });
  map.addControl(new OpenLayers.Control.Navigation());

  var gsat = new OpenLayers.Layer.Google(
    "Google Satellite",
    {type: google.maps.MapTypeId.SATELLITE, numZoomLevels: 22}
  );

  map.addLayers([gsat]);
  map.zoomToMaxExtent();
}
 


function loadPage(options) {
  
  var map = loadMap("map"); 

  $( "#tabs" ).tabs();
  $("#tabs-1").removeClass("ui-corner-bottom");

  $( ".tabs-bottom .ui-tabs-nav, .tabs-bottom .ui-tabs-nav > *" )
    .removeClass( "ui-corner-all ui-corner-top" )
    .addClass( "ui-corner-bottom" );

  $(".tool-controls").button({ 
    icons: { 
      secondary: "ui-icon-triangle-1-s"}
  });
   
  $(".tool-controls").click(function() { 
    $(this).find("ul").width($(this).width()-14).css({'margin-left':'-5px'});
    $(this).find("ul").toggle();
  })

  var grid = loadGrid(options); 

  $('#removeMeter').click(function(){ 
    var remove = confirm("Are you sure that you want to remove this meter?"); 
    if (remove) {       
      window.location = "/meter/remove/" + options.meter
    } else {};     
  }); 


  function flashMessage(msg) { 
    $("<div />", {id : "flashMessage", })
  }; 

  $('#addCircuitButton').click(function() { 
    $('#addCircuit').dialog({
      title: "Add circuit to meter",
      modal: true,
      buttons: { 
        "Add new circuit": function() { 
          $.ajax({ 
            url: "/meter/add_circuit/" + options.meter,
            data: $("#add-circuit").serialize(),
            type: "POST",
            success: function(response) { 
              $("#addCircuit").dialog("close");
              $("<div />", {id : "dialog"}).text();
            },
            error: function(response) { 
              alert(response); 
            }
          })


        },
        "Cancel" : function() { 
          $(this).dialog("close"); 
        }
      }
    });               
  });

}; 
