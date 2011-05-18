<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
   <%namespace name="headers" file="headers.mako"/>
   ${headers.globalScripts(request)}   
   ${headers.styleSheets(request)} 
   ${self.header()}

  </head>
  <body>
      <%! 
         from datetime import datetime         
      %>
      <div id="clock">        
        <p><strong>${datetime.now().ctime()}</strong></p>
      </div>

    <div class="container">
      <div class="header">
        <h1><a href="/"> SharedSolar Gateway</a></h1>
      </div>

      <div class="navigation">
        <ul class="menu">
          <li > <a href="#">Dashboard</a></li>
          <li class="ui-state-default ui-corner-top ui-tabs-active">
            <a href="/">Manage</a></li>
        </ul>
      </div>
        <ol class="breadcrumbs ui-widget-header ui-corner-top">

        % if breadcrumbs:
            % for crumb in breadcrumbs: 
                % if crumb.get("url"):
                   <li>&#187; <a href="${crumb.get("url")}"> 
                    ${crumb.get("text")}</a></li>
                % else:
                    <li class="active">&#187; ${crumb.get("text")}</li> 
               % endif
            % endfor 
        % endif 

        <div id="auth">
        % if user: 
             <span>Hi ${user}</span> | 
             <a href="/user/profile">Edit profile</a> | 
             <a href="${a_url}/user/logout">Log out</a>
        % else: 
              <a href="${a_url}/user/login?came_from=${request.path}">
                Log in</a>
       % endif 
        </div>

        </ol>
        <div class="ui-widget ui-widget-content content">
          ${self.content()}
        </div>
    </div>
  </body>  
</html>

