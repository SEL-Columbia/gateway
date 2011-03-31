<%inherit file="../base.mako"/>

<%def name="header()">
   <title>User profile for ${user}</title>
</%def>

<%def name="content()">
     <h3>Update your password</h3>
     % if error:
         ${error}
     % endif
     <form method="POST" id="" action="${a_url}/user/profile">
       <table>
         <tr>
           <td><label> Old password</td></td>
           <td><input type="password" name="old_password" value="" /></td>
         </tr>
         <tr>
           <td><label>New password</label></td>
           <td><input type="password" name="new_password" value="" /></td>
         </tr>
         <tr>
           <td><label>Verify new password</label></td>
           <td><input type="password" name="verify_password" value="" /></td>
         </tr>
         <tr>
           <td></td>
           <td><input type="submit" name="" value="Update password" /></td>
         </tr>
       </table>
     </form>
</%def>
