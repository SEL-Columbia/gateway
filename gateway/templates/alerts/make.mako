<%inherit file="../base.mako"/>

<%def name="header()">
  <title>Send Alerts</title>
</%def>

<%def name="content()">
 <h2>Send Test Message</h2>
 
 <p>Send message via the follow interface</p>

 <form method="POST" id="" 
       action="${request.application_url}/alerts/send_test">
   <table>
     <tr>
       <td>
       <select name="interface">
         % for interface in interfaces:
         <option value="${interface.id}">${interface.name}</option>
         % endfor     
       </select>
       </td>
      </tr>
     <tr>
       <td>
       <input type="text" name="number" value="" />
       </td>
     </tr>
     <tr>
       <td>
         <textarea name="text" rows="4" cols="20" >
         </textarea>
       </td>
     </tr>
     <tr>
       <td>
         <input type="submit" name="submit" value="Send Message" />
       </td>
     </tr>
   </table>
 </form>
 
</%def>
