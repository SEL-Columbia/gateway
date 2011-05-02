<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title></title>
    <script type="text/javascript"
            src="${a_url}/static/js/jquery-1.4.3.min.js">
    </script>

    <script type="text/javascript" 
            src="${a_url}/static/js/openlayers/OpenLayers.js">
    </script>
    <script type="text/javascript" 
            src="${a_url}/static/js/maps.js">
    </script>

    <link rel="stylesheet" 
          href="${a_url}/static/js/openlayers/theme/default/style.css"
          type="text/css" />

    <script src="http://maps.google.com/maps/api/js?sensor=false"></script>

    <style type="text/css" media="screen">
      #map { 
        background: #eee;
        width: 100%; 
        height: 600px;
      } 
    </style>

  </head>
  <body>
    <div id="map">
    </div>
    <a id="select" href="#">Select Features</a>
    <a id="pan" href="#">Pan Map</a>
  </body>
</html>
