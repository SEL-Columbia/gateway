<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>

<%def name="header()">
${headers.loadSlickGrid(request)} 

<script type="text/javascript" 
        src="${a_url}/static/js/d3/d3.js">
</script>


<link rel="stylesheet" 
      href="${a_url}/static/js/openlayers/theme/default/style.css" type="text/css" />

<script src="http://maps.google.com/maps/api/js?sensor=false"></script>

<script type="text/javascript" 
        src="${a_url}/static/js/openlayers/OpenLayers.js">
</script>

<script type="text/javascript"
        src="${a_url}/static/js/site/meterPage.js"></script>

<style type="text/css" media="screen">
  	.tabs-bottom { position: relative; } 
	.tabs-bottom .ui-tabs-panel { height: 140px; overflow: auto; } 
	.tabs-bottom .ui-tabs-nav { position: absolute !important; 
        left: 0; bottom: 0; right:0; padding: 0 0.2em 0.2em 0; } 
	.tabs-bottom .ui-tabs-nav li { margin-top: -2px !important; 
        margin-bottom: 1px !important; border-top: none; border-bottom-width: 1px; }
        #tabs { 
           width: 900px;
           height: 350px;
           float: right; 
        } 
</style>

<script type="text/javascript">
  $(function() { 
    loadPage({ 'meter' : ${meter.id}, 
               'main': ${meter.getMainCircuitId()},
               'geometry': "${meter.geometry}"});
  });
</script>
</%def>

<%def name="content()">

  <div style="float: right">
      <a id="tool-control" href="#">Manage meter information</a>
  </div>
  <div id="tool-menu" class="ui-corner-all ui-widget" 
       style="display:none">

    <ul>      
      <li>
        <a id="edit" href="${meter.edit_url()}">Edit meter description</a>
        <p>Page to allow users to edit and update meter
          information</p>
      </li>
      <li>
        <a id="editMeterConfig" href="#">Edit meter configuration</a>
        <p>Widget that allows admins to update remote meter
        information</p>
      </li>
      <li>
        <a id="removeMeter" href="#">Remove Meter</a>
        <p>Remove the meter from the databae</p>
      </li>
      <li>
        <a id="addCircuitButton" href="#">Add Circuit</a>
        <p> Widget to allow admins to add circuits to this meter</p>
      </li>
    </ul>
    <ul>
      <li>
        <a href="${a_url}/meter/message_graph/${meter.id}">Meter messages</a>
        <p>Table that displays all of the meter information</p>
      </li>
      <li>
        <a href="${a_url}/meter/ping/${meter.id}">Ping Meter</a>
        <p>Sends a job to the meter to check meter's status</p>
      </li>
    <ul>
  </div>



<h3>Meter overview page for <span class="underline">${meter.name}</span></h3> 

<div id="tabs" class="tabs-bottom">
	<ul>
	  <li><a href="#map-tab">Map</a></li>          
	  <li><a href="#graph-tab">Daily Accumulated Energy Graph</a></li>
	</ul>
	<div id="map-tab">
          <div id="map"></div>
	</div>
	<div id="graph-tab">
          <div>    
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
            <div id="graph" style="height: 300px;">
            </div>
</div>

	</div>
</div>


<ul class="overview">
  <li>
    <h4>Meter Name</h4>
    <p>${meter.name}</p>
  </li>
  <li>
    <h4>Meter location</h4>
    <p>${meter.location}</p>
  </li>
  <li>
    <h4>Meter phone</h4>
    <p>${meter.phone}</p>
  </li>
  <li>
    <h4>Meter status</h4>
    <p>${meter.status}</p>       
  </li>
  <li>
    <h4>Time of last report</h4>
         <p> TBD </p>
  </li>
</ul>

<div class="grid">
  
  <div id="circuit-grid"></div>
</div>
<!-- 
     Update meter configuration
-->
<div id="updateMeterConfig" style="display:none;">
  <p> This form allows users to update the remote configuration on a
  meter.</p>
  <form method="" id="configForm" action="">
    <select name="key">
      % for key in meter_config_keys:
         <option value=${key.id}> ${str(key)} </option>
      % endfor
    </select>
  </form>
  <hr />
  <p>Change sets associated with this meter</p>
  % for change in changesets:
     ${change}
  % endfor
</div>
<!-- 
     Added new circuit form
--> 

<div id="addCircuit" style="display: none">
  <form  id="add-circuit">
  <table>
    <tr>
      <td><label>Account language</label></td>
      <td>
        <select name="lang" id="lang"> 
          <option value="en">English</option>
          <option value="fr">French</option>
        </select>
      </td>
    </tr>
    <tr>
      <td><label>Account Phone</lable></td>
      <td><input type="text" id="phone" name="phone" value="" /></td>      
    </tr>

    <tr>
      <td><label>Ip Address: </label></td>
      <td><input type="text" id="ip_address" name="ip_address" 
                 value="192.168.1.201" /></td>
    </tr>
    <tr>
      <td><label>Circuit pin: </label></td>
      <td><input type="text" id="pin" name="pin" 
                 value="" /></td>
    </tr>
    <tr>
      <td><label>Energy Max: <label></td>
      <td><input type="text" id="energy_max" name="energy_max" value="100"
      /></td>      
    </tr>
    <tr>
      <td><label>Power Max: </label></td>
      <td><input type="text" id="power_max"  name="power_max" value="100"
      /></td>
    </tr>
</table>
</form>
</div> 


</%def> 
