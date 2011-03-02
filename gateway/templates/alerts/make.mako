<%inherit file="../base.mako"/>

<%def name="header()">
  <title>Send Alerts</title>
</%def>

<%def name="content()">
 <h2>Send Test Message</h2>
 
 % for interface in interfaces:
     ${interface.name}
 % endfor
 
 <form method="POST" id="" action=".">
   <select name="interface">
   </select>
 </form>
 
</%def>
