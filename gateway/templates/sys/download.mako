<%inherit file="../base.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>
</%def>

<%def name="content()">
<h2>Export database tables</h2>

<form method="POST" id=""
      action="${request.application_url}/sys/export">
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
        <input type="submit" name="" value="Export data" />
      </td>
    </tr>
  </table>
</form>
<hr />
<h3>Documentation</h3>
<p>It is possible to download the info via command line. For example
  using curl one could download all of the jobs.</p>

<code>
curl -XGET ${request.application_url}/sys/export?model=Jobs
</code>

</%def>
