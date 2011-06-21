<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>

<%def name="header()"> 

    <title>Circuit Page</title>
    ${headers.loadSlickGrid(request)}
    <script type="text/javascript" 
            src="${a_url}/static/js/d3/d3.js">
    </script>
    <script type="text/javascript"
            src="${a_url}/static/js/site/circuitPage.js">
    </script>
    <script type="text/javascript">
      $(function() { 
         loadPage({circuit: "${circuit.id}" });
         $("#update-graph").button();
      });      
    </script>

    <style type="text/css" media="screen">
      #graph { 
        margin-top: 80px;
        margin-bottom: 10px;
        height: 400px;
        width: 100%;
      } 
      
    </style>
</%def> 

<%def name="content()"> 
<h3>Circuit overview page</h3>
<ul class="overview">
  <li>
    <h4>Circuit id</h4>
    <p>${circuit.id}</p>
  </li>        
  <li>
    <h4>Circuit meter</h4>
    <p> <a href="${a_url}/meter/index/${circuit.meter.id}">${circuit.meter}</a>
  <li>
    <h4>Circuit credit</h4>
    <p>${circuit.credit}</p>
  </li>
  <li>
    <h4>Circuit account number</h4>
    <p>${circuit.pin}</p>
  </li>
  <li>
    <h4>Circuit account phone number</h4>
    <p>${circuit.account.phone}</p>
  </li>
</ul>

<p>Select value to graph</p>
<form method="GET" id="date-ranges" action="">
  <select name="value">
    <option value="watthours">Watt hours</option>
    <option value="credit">Credit</option>
    <option value="use_time">Use time</option>
  </select>

<%! 
  from datetime import datetime, timedelta
  now = datetime.now() + timedelta(days=1)
  last_week = now - timedelta(days=7)
%>
  <p>Select date range</p>
  <input id="start" type="text" name="start"
         value="${last_week.strftime("%m/%d/%Y")}" />
  <input id="end" type="text" name="end" value="${now.strftime("%m/%d/%Y")}" />
</form>
<a id="update-graph">Update Graph</a>


<div id="graph">
  <div id="ajax-loader">
    <img src="${a_url}/static/images/ajax-loader.gif" class="" alt="" />
  </div>
</div>

<div id="tool-menu" class="ui-corner-all ui-widget">
  <ul> 
    <li>
      <a href="${a_url}${circuit.edit_url()}">Edit circuit
      information</a>
      <p>Edit and update information about this circuit</p>
    </li> 
    <li>
      <a href="${a_url}/account/edit/${str(circuit.account.id)}">Edit
        account information</a>
      <p>Edit information associated with this circuits's account</p>
    </li>
    <li>
      <a id="removeCircuit" href="#">Remove circuit</a>
      <p>Removes the circuit from the database, cannot be undone</p>
    </li>
  </ul>
  <ul>
    <li>
      <a href="${a_url}/circuit/turn_on/${circuit.id}">Turn On</a>
      <p>Creates a job that turns the circuit on</p>
    </li>
    <li>
      <a href="${a_url}/circuit/turn_off/${circuit.id}">Turn Off</a>
      <p>Creates a job that turns the circuit off</p>
    </li>
    <li>
      <a href="${a_url}/circuit/ping/${circuit.id}"> Ping Circuit </a>
      <p>Sends a job to check the status of the circuit</p>
    </li>
    <li>
      <a href="#">Add credit to account</a>
      <p>Sends a job to meter to add credit to a circuit</p>
      <form method="POST" id=""
            action="${a_url}/circuit/add_credit/${circuit.id}">
        <input type="text" name="amount" value="" />
        <input type="submit" name="" value="Add credit to account" />
      </form>
    </li>
  </ul>
</div>

<div id="logs">
  <ul>
    <li><a href="#primary-logs">Circuit Logs</a></li>
    <li><a href="#billing-history">Billing history</a></li>
  </ul>

  <div id="primary-logs">    
  </div>
  <div id="billing-history">
  </div>
  
</div>

</%def> 
