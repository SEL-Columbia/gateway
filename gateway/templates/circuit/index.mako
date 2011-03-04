<%inherit file="../base.mako"/>

<%def name="header()"> 
    <title>Circuit Page</title>
    <script type="text/javascript">
      $(function() { 
         $('.buttons li').button()
      });
      
    </script>
</%def> 

<%def name="content()"> 
<h3>Circuit overview page</h3>

<table class="no-border" border="0">
  <tr>
    <td>
      <table class="overview">
      % for key,value in fields.iteritems(): 
      <tr>
        <td class="hint">Circuit ${key}</td>
        <td>${str(value.get("value"))}</td>
      </tr>
      % endfor 
        <tr>
          <td class="hint">Account phone</td>
          <td><a href="${request.application_url}/${circuit.account.url()}">${str(circuit.account.phone)}</a></td>
        </tr>
        <tr>
          <td class="hint">Account language</td>
          <td>${circuit.account.lang}</td>
        </tr>
      </table>
    </td>    
    <td>
      <div class="buttons">        
      <ul> 
        <li><a 
               href="${request.application_url}${circuit.edit_url()}">
            Edit circuit information</a></li> 
        <li>
          <a href="${request.application_url}/account/edit/${str(circuit.account.id)}">
            Edit account information</a></li>
        <li><a href="${circuit.remove_url()}">Remove circuit</a></li>
        <li>
          <a href="${request.application_url}/circuit/turn_on/${circuit.id}">
            Turn On </a>
        </li>
        <li>
          <a href="${request.application_url}/circuit/turn_off/${circuit.id}">
            Turn Off </a>
        </li>
        <li>
          <a href="${request.application_url}/circuit/ping/${circuit.id}">
            Ping Circuit </a>
        </li>
        <li>
          <form method="POST" id=""
                action="${request.application_url}/circuit/add_credit/${circuit.id}">
            <label>Amount</label>
            <input type="text" name="amount" value="" />
            <input type="submit" name="submit" value="Add credit" />
          </form>
        </li>
      </ul>
      <img 
         src="${request.application_url}/graph/Circuit/${circuit.id}?column=credit&figsize=7,4" class="" alt="" />
      <p>Graph by 
        <a href="#">Credit</a> | 
        <a href="#">Watt hours</a> |
        <a href="#">Use Time </a>
      </div>
    </td>
  </tr>

</table>
<hr />
<h4>Jobs associated with circuit</h4>
<a 
   href="${request.application_url}/circuit/remove_jobs/${circuit.id}">
   Clear job queue</a>
${jobs.render()}
<hr /> 
<h4>All of the logs associated with circuit</h4>
${logs.render()}
</%def> 
