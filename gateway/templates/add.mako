<%inherit file="base.mako"/>

<%namespace name="headers" file="headers.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
   ${headers.deformStyles(request)}
</%def>

<%def name="content()"> 
   <h3>Add a new ${cls.__name__}</h3>
   <form method="POST" id="" 
         action="${request.application_url}/add/${cls.__name__}">
     ${fs.render()}
     <input type="submit" name="submit" value="Add new ${cls.__name__}" />
   </form>
</%def>
