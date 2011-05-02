<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>Please log in</title>

   <%namespace name="headers" file="headers.mako"/>   
   ${headers.styleSheets(request)} 

   <style type="text/css" media="screen">
     h3 { margin: 5px;} 
     #login-form { 
        margin: 10px auto; 
        width: 500px;
     } 
     
   </style>

  </head>
  <body>
    <div id="login-form">
      <div class="ui-widget-header ui-corner-top">
        <h3>Please login</h3>
      </div>
      <div class="ui-widget ui-widget-content padding">
        <div class="error"><p>${message}</p></div>
        <form method="POST" id=""
              action="${request.application_url}/user/login">
          <table>
            <tr>
              <td><label>Username</label></td>
              <td><input type="text" name="name" value="" /></td>
            </tr>
            <tr>
              <td><label>Password</label>
              <td><input type="password" name="password" value="" /></td>          
            <tr>
              <td></td>
              <td> 
                <input type="submit" name="form.submitted" value="Log in"/>
              </td>
          </table>
          <input type="hidden" name="came_from" value="${came_from}" />
        </form>
      </div>
    </div>
  </body>
</html>
