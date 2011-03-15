<%inherit file="../base.mako"/>

<%def name="header()"> 
    <title>Circuit Page</title>
    <script type="text/javascript">
      var graph, column, app, circuit;    
      app = "${a_url}";
      circuit = "${circuit.id}";
      graph = $('#graph-image');

      $(function() { 
         $('.buttons li').button()
         $('.graph-tools a').click(function() { 
           column = $(this).attr('id');
           var url = app + "/graph/Circuit/" + circuit  + "?column=" + column +"&figsize=7,4";
           $("#graph-image").attr('src', url);
         })
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
         id="graph-image"
         src="${a_url}/graph/Circuit/${circuit.id}?column=watthours&figsize=7,4" />

      <p>Graph by
        <div class="graph-tools">
          <a id="credit" href="#">Credit</a> | 
          <a id="watthours" href="#">Watt hours</a> |
          <a id="use_time" href="#">Use Time </a>
        </div>
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
