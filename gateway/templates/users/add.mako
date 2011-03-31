<%inherit file="../base.mako"/>

<%def name="header()">
   <title>Add a new user</title>
</%def>

<%def name="content()">
   <h3>Add a new user</h3>
   <form method="POST" id="" action="${a_url}/user/add">
     <table>
       <tr>
         <td><label>Username</label></td>         
         <td><input type="text" name="name" value="" /></td>
       </tr>
       <tr>         
         <td><label>Email address </label> </td> 
         <td><input type="text" name="email" value="" /></td>
       </tr>
       <tr>
         <td><label>Password</label></td>
         <td><input type="password" name="password" value="" /></td>
       </tr>
       <tr> 
         <td><label>User group</label></td>
         <td>
           <select name="group"> 
             % for group in groups: 
                <option value="${group.id}">${group.name}</option>
             % endfor 
           </select>
         </td>
       </tr>
       <tr> 
         <td></td>
         <td><input 
                 type="submit" 
                 name="submit" 
                 value="Add new user"/>
         </td>
       </tr>
     </table>
   </form>
</%def>

