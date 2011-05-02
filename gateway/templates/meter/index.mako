<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>

<%def name="header()">
${headers.loadSlickGrid(request)} 

<link rel="stylesheet" 
      href="${a_url}/static/js/openlayers/theme/default/style.css" type="text/css" />

<script src="http://maps.google.com/maps/api/js?sensor=false"></script>

<script type="text/javascript" 
        src="${a_url}/static/js/openlayers/OpenLayers.js">
</script>

<script type="text/javascript" 
        src="${a_url}/static/js/site/jquery.tmpl.js.js"></script>

<script type="text/javascript" 
        src="${a_url}/static/js/datastore.js"></script>

<script type="text/javascript" 
        src="${a_url}/static/js/grid.js"></script>

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
     loadPage({ 'meter' : ${meter.id}, 'geometry': "${meter.geometry}"});
  });
</script>
</%def>

<%def name="content()">

  <div id="tools" class=""> 
    <ul class="tool-box" id="edit-box">
      <li class="tool-controls" >
        <a href="#">Manage meter information</a>
        <ul style="display:none">         
          <li>
                <a id="edit" href="${meter.edit_url()}">Edit meter information</a>
          </li> 
          <li>
            <a id="removeMeter" href="#">Remove Meter</a>
          </li>
          <li>
            <a id="addCircuitButton" href="#">Add Circuit</a>
          </li>
        </ul>
      </li>
      <li class="tool-controls">
        <a  href="#">Download information</a>
        <ul style="display:none">
          <li>
            <a id="accounts" 
               href="${a_url}/meter/show_account_numbers/${meter.id}">
              Download accounts</a>
          </li>
          <li><a id="showAlerts"href="#">Show alerts</a></li>
          <li><a id="messages" href="#">Message table</a></li>
        </ul>
      </li>
      <li class="tool-controls">
        <a  href="#">Create job</a>
        <ul style="display:none">
          <li>
            <a id="ping" href="${a_url}/meter/ping/${meter.id}">Ping</a>
          </li>
        </ul>
      </li>
    </ul>
  </div>



<h3>Meter overview page for <span class="underline">${meter.name}</span></h3> 

<div id="tabs" class="tabs-bottom">
	<ul>
	  <li><a href="#tabs-1">Map</a></li>          
	  <li><a href="#tabs-2">Power Graph</a></li>
	</ul>
	<div id="tabs-1">
          <div id="map"></div>
	</div>
	<div id="tabs-2">
          <div id="graph">
            <img 
               src="${a_url}/graph/Circuit/${meter.getMainCircuit().id}?column=watthours&figsize=8,3" class="" alt="" />
          </div>
	</div>
</div>



<ul id="meter-overview">
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

<h4>Circuits associated
  with <span class="underline">${meter.name}</span></h4>

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
<div id="grid"></div>

</%def> 
