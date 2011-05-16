var grid, vector_layer;
function loadGrid(options) { 

  var gridOptions = {
    forceFitColumns: false,
    autoHeight: true,
    enableCellNavigation: true,
    enableColumnReorder: true
  };

  function CircuitLinkFormatter(row, cell, value, columnDef, data) { 
    return "<a href=\"/circuit/index/" + data.id + "\">" + value + "</a>";
  }; 
  
  var columns = [ 
    {id: "ip_address",width: 100, name: "Ip Address", 
     field: "ipaddress", sortable:true},
    {id: "account", name: "Account", 
     formatter: CircuitLinkFormatter, field: "account", sortable:true},
    {id: "last_msg",width: 200, name: "Last Messages", 
     field: "last_msg", sortable:true},
    {id: "status", name: "Status",  formatter:BoolCellFormatter, 
     field: "status", sortable: true },
    {id: "language", name: "Language", field: "language", sortable:true},
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

function loadMap(div, options) {
  var geographic = new OpenLayers.Projection("EPSG:4326");
  var googleProj = new OpenLayers.Projection("EPSG:900913");
  var bounds = new OpenLayers.Bounds(
        -20037508, -20037508, 20037508, 20037508.34
  ); 

  var map = new OpenLayers.Map('map', {
    projection: googleProj,
    maxResolution: 156543.0339,
    controls: [],
    maxExtent: bounds
    });

  map.addControl(new OpenLayers.Control.Navigation());

  var gsat = new OpenLayers.Layer.Google(
    "Google Satellite",
    {type: google.maps.MapTypeId.SATELLITE, 
     'sphericalMercator': true,
     numZoomLevels: 22}
  );
  map.addLayers([gsat]);

  var WKT = new OpenLayers.Format.WKT();
  var geom = WKT.read(options.geometry);
  if (options.geometry !== 'None') { 
    geom.geometry.transform(geographic, googleProj);
    var style = new OpenLayers.StyleMap({ 
      'default': new OpenLayers.Style({           
        pointRadius: 10,
        fillColor: '#CD0707',
        strokeColor: '#004276'
      })
    })
    var vector_layer = new OpenLayers.Layer.Vector('Meter', { 
      styleMap: style,
    });
    map.addLayer(vector_layer);
    vector_layer.addFeatures(geom);  
    map.setCenter(new OpenLayers.LonLat(geom.geometry.x, geom.geometry.y), 17);

  } else { 
    map.zoomToExtent(bounds);
  }
 
  return map;
}
 

var map;
function loadPage(options) {
  
  map = loadMap("map", options); 

  $( "#tabs" ).tabs();
  $("#tabs-1").removeClass("ui-corner-bottom");
  

  $( ".tabs-bottom .ui-tabs-nav, .tabs-bottom .ui-tabs-nav > *" )
    .removeClass( "ui-corner-all ui-corner-top" )
    .addClass( "ui-corner-bottom" );

  $(".tool-controls").button({ 
    icons: { 
      secondary: "ui-icon-triangle-1-s"}
  });
   
  $(".tool-controls").click(function(evt) { 
    $(this).find("ul").width($(this).width()-14).css({'margin-left':'-5px'});
    $(this).find("ul").toggle().css("margin-top",10).height(100);
    $(this).find("ul").menu();
    $(this).find("ul").css("position","absolute");
  })

  var grid = loadGrid(options); 

  $('#removeMeter').click(function(){ 
    var remove = confirm("Are you sure that you want to remove this meter?"); 
    if (remove) {       
      window.location = "/meter/remove/" + options.meter
    } else {};     
  }); 

  
  $("#editMeterConfig").click(function() { 
    $("#updateMeterConfig").dialog({ 
      title: 'Update remove meter config',
      width: 400,
      zIndex: 2000,
      modal: true,
      buttons: { 
        'Update key': function() { 
          console.log($(""))
        }
      }
    });
  })


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
