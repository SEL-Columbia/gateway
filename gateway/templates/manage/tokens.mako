<%inherit file="../base.mako"/>

<%def name="header()">
  <title>Manage Tokens</title>
   <script type="text/javascript">
     $(function() { 
        $('.button').button(); 
     }); 
   </script>
</%def>

<%def name="content()">
  <form method="POST" id=""
        action="${a_url}/manage/add_tokens">
    <table>
      <tr>
        <td class="hint">Number of tokens to be create</td>
        <td><input type="text" name="amount" value="" /></td>
      </tr>
      <tr>
        <td class="hint">Value for each token</td>
        <td><input type="text" name="value" value="" /></td>
      </tr>
      <tr>
        <td></td>
        <td><input class="button" 
                   type="submit" 
                   name="" 
                   value="Add token" /></td>
      </tr>
    </table>
  </form>
  <h4>Upload tokens from csv</h4>
  <form method="POST" id=""
        enctype="multipart/form-data"
        action="${a_url}/manage/upload_tokens">
    <input type="file" name="csv" value="" />
    <input class="button" 
           type="submit" 
           name="submit" 
           value="Upload tokens from csv" />
  </form>
  <hr /> 
  ${grid.render()}
</%def>
