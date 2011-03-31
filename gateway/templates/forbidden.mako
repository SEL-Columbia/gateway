<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>Not Allowed</title>

   <%namespace name="headers" file="headers.mako"/>   
   ${headers.styleSheets(request)} 

   <style type="text/css" media="screen">
     h3 { margin: 5px } 
     #center-box { 
        margin: 10px auto; 
        width: 500px;
        background: #E5ECF9; 
     }
     #box-content { 
        padding: 8px;
     } 
   </style>

  </head>
  <body>
    <div id="center-box">
      <div class="ui-widget-header ui-corner-all">
        <h3>You are not allowed to access that page!</h3>
      </div>
      <div id="box-content">
      <p>Reason:</p>
      % if logged_in:
         <p>You are logged in, but lack sufficient privileges.</p>
      % else: 
         <p>You are not logged in, please do so now. 
           <a href="${a_url}/user/login?came_from=${request.path}">Log in</a></p>
      % endif
      </div>
    </div>
  </body>
</html>
