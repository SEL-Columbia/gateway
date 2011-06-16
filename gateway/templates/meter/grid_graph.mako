<%namespace name="headers" file="../headers.mako"/>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>Grid Graph</title>
   ${headers.globalScripts(request)}   
   ${headers.styleSheets(request)} 
   ${headers.loadSlickGrid(request)}

    <script type="text/javascript" 
            src="${a_url}/static/js/d3/d3.js">
    </script>
    <script type="text/javascript" src="${a_url}/static/js/site/meterGridGraph.js"></script>
    <script type="text/javascript">
      $(function() { 
         loadPage({ 
           circuits: ${ [c.id for c in meter.get_circuits()]}
         })      
      });
    </script>
    <style type="text/css" media="screen">
      body { margin: 0px; }
      #con { margin: 10px; auto; } 
      #grids {
      } 
      #form { margin: 5px;} 
      .circuit_grid {          
         float: left;
         height: 300px;
         width: 300px;
         margin: 5px;
         border: 1px solid #808080;
         text-align: center;
      } 
      .ajax_loader { 
        margin-top: 150px;
      } 
    </style>
  </head>

<%! 
  from datetime import datetime, timedelta
  now = datetime.now() + timedelta(days=1)
  last_week = now - timedelta(days=7)
%>

  <body>
    <div id="con">
    <div id="form"> 
      <form method="" id="" action="">
        <input type="text" name="start" value="${last_week.strftime("%m/%d/%Y")}" />
        <input type="text" name="end" value="${now.strftime("%m/%d/%Y")}" />
        <a href="#">Upgrade graph</a>
      </form>
    </div>
    <div id="grids"> </div>
    </div>
  </body>
</html>
