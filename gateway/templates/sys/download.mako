<%inherit file="../base.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
   <script type="text/javascript">
     $(function(){ 
        $(".button").button();
       });
   </script>
</%def>

<%def name="content()">
<h2>Export database tables</h2>

<form method="POST" id=""
      action="${request.application_url}/system/export">
  <table>
    <tr>
      <td><label>Database table</label></td>
      <td>
        <select name="model">
          % for table in tables:
          <option value="${table.__name__}"> ${table.__name__}</option>
          %endfor
        </select>
      </td>
    </tr>
    <tr>
      <td><label>Export type</label></td>
      <td>
        <select name="format">
          <option value="csv"> CSV</option>
        </select>
      </td>        
    </tr>
    <tr>
      <td></td>
      <td>
        <input class="button"
               type="submit" name="" value="Export data" />
      </td>
    </tr>
  </table>
</form>
<hr />
<h3>Documentation</h3>
<p>It is possible to download the info via command line. For example
  using curl one could download all of the jobs.</p>
<br/>
  
<code>
    curl -XGET ${request.application_url}/system/export?model=Jobs
</code>

</%def>
