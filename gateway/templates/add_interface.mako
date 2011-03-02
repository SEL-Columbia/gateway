<%inherit file="base.mako"/>

<%namespace name="headers" file="headers.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
   ${headers.deformStyles(request)}
</%def>

<%def name="content()"> 
   <br />
   <form method="POST" id="" 
         action="${request.application_url}/add/${cls}">
     ${fs.render()}
     <input type="submit" name="submit" value="Add new ${cls.__name__}" />
   </form>
</%def>
