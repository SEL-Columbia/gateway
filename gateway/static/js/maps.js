var map;
$(function() { 
  var geographic = new OpenLayers.Projection("EPSG:4326");
  var googleProj = new OpenLayers.Projection("EPSG:900913");
  var bounds = new OpenLayers.Bounds(
        -20037508, -20037508, 20037508, 20037508.34
  ); 

  map = new OpenLayers.Map('map', {
    projection: googleProj,
    maxResolution: 156543.0339,
    controls: [],
    maxExtent: bounds
    });
  
  map.addControl(new OpenLayers.Control.PanZoom());
  map.addControl(new OpenLayers.Control.Navigation());

  var gsat = new OpenLayers.Layer.Google(
    "Google Satellite",
    {type: google.maps.MapTypeId.SATELLITE, 
     'sphericalMercator': true,
     numZoomLevels: 22}
  );
  map.addLayers([gsat]);

  var style = new OpenLayers.StyleMap({ 
    'default': new OpenLayers.Style({ 
      labelYOffset: 30,
      fontColor: "#fff",
      pointRadius: 7,
      fillColor: '#820BBB',
    }),
    'select': new OpenLayers.Style({
      pointRadius: 7,
      fillColor: "#E32E30"
    })
  })
  
  var meters = new OpenLayers.Layer.Vector(
    "Meters", { 
      projection: new OpenLayers.Projection("EPSG:4326"),
      styleMap: style,
      strategies: [
        new OpenLayers.Strategy.Cluster(),
        new OpenLayers.Strategy.Fixed()],
      protocol: new OpenLayers.Protocol.HTTP({ 
        url: "/manage/metersAsGeoJson",
        format: new OpenLayers.Format.GeoJSON()
      })
    }    
  )
  map.addLayer(meters);

  var selectControl = new OpenLayers.Control.SelectFeature(meters, 
    {
      box: true    }
  )

  map.addControl(selectControl);
  
  $("#select").click(function() { 
    selectControl.activate();
  })
  
  $("#pan").click(function() { 
    selectControl.deactivate();
  });

  meters.events.on({ 
    'featureselected': function(event) { 
      $("<div />", {id: "popup"});
      $("#popup").dialog(event);
    }
  })

  map.zoomToExtent(new OpenLayers.Bounds(
      -4006523.2738786, -2191602.4746, 8213617.3099402, 3678761.29665
  ));

});
