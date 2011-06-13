<%inherit file="base.mako"/>

<%namespace name="headers" file="headers.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
</%def>

<%def name="content()"> 
   <h3>Editing <span class="underline">${str(instance)}</span> </h3>
   <form method="POST" id="" 
         action="${request.application_url}/edit/${cls.__name__}/${instance.id}">
     ${fs.render()}
     <input type="submit" name="submit" value="Update ${cls.__name__}" />
   </form>
</%def>
