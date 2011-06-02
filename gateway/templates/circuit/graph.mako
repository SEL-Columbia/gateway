<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>Circuit Graph</title>

    <%namespace name="headers" file="../headers.mako"/>
    ${headers.globalScripts(request)}
    ${headers.styleSheets(request)} 

    <script type="text/javascript" 
            src="${a_url}/static/js/d3/d3.js">
    </script>
    <script type="text/javascript"
            src="${a_url}/static/js/site/circuitGraph.js">
    </script>
    <style type="text/css" media="screen">
      #main {
         margin: 10px auto;
         width: 1000px;
      } 
    </style>

  </head>
  <body>
    <div id="main">
      <div id="graph"></div>
      <hr />
      <form method="GET" id="date-ranges" action="">
        <input id="start" type="text" name="start" value="" />
        <input id="end" type="text" name="end" value="" />      
      </form>
      <a id="update-graph" href="#">Update Graph</a>
    </div>
  </body>
</html>
