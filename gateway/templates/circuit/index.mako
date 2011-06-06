<%inherit file="../base.mako"/>

<%def name="header()"> 
<%namespace name="headers" file="../headers.mako"/>
    <title>Circuit Page</title>
    ${headers.loadSlickGrid(request)}

    <script type="text/javascript" 
            src="${a_url}/static/js/d3/d3.js">
    </script>

    <script type="text/javascript"
            src="${a_url}/static/js/site/circuitPage.js"></script>

    <script type="text/javascript">
      $(function() { 
         loadPage({circuit: "${circuit.id}" });
      });      
    </script>
    <style type="text/css" media="screen">
      #graph { 
        margin-top: 40px;
        margin-bottom: 10px;
        height: 400px;
        width: 100%;
        background: #eee;
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

<div id="graph"></div>

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
    </li>
  </ul>
</div>

<div id="logs">
  <ul>
    <li><a href="#primary-logs">Circuit Logs</a></li>
    <li><a href="#alarms">Alarms</a></li>
  </ul>

  <div id="primary-logs">    
  </div>
  <div id="alarms">
  </div>
  
</div>
</%def> 
