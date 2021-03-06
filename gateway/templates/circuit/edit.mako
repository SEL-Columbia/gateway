<%inherit file="../base.mako"/>

<%def name="header()"> 
    <title>Circuit Page</title>
</%def> 

<%def name="content()"> 
<h3>Edit circuit ${circuit.pin}</h3>
<a 
   href="${request.application_url}${circuit.url()}">Back to circuit page</a>
<table class="form">
<form method="POST" id="" 
      action="${request.application_url}/circuit/update/${circuit.uuid}">
  
  % for key,value in fields.iteritems(): 
  
  % if key != "Meter":
     <tr>
       <td><label>${key}</label></td>
       <td><input type="text" 
                  name="${key.lower()}" 
                  value="${value.get("value")}" /></td>
       % endif
       
     </tr>
  % endfor   
     <tr>
       <td></td>
       <td>
         <input type="submit" 
                name="submit" 
                value="Update circuit" /></td>
     </tr>
</form>
</table>

</%def> 
