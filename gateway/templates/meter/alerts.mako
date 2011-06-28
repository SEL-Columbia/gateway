<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>

<%def name="header()">
<style type="text/css" media="screen">
  #alerts { 
    list-style: none;
  }
  #alerts li { 
    margin: 10px;
    padding: 10px;
  } 
</style>
</%def>    

<%def name="content()">
<ul id="alerts">
  % for alert in alerts: 
  <div class="ui-widget">
    <li class="ui-state-highlight ui-corner-all">
      <h4>Alert ${alert._type}</h4>
      <p>Alert date <strong> ${alert.date.ctime()}</strong></p>
      <p>Circuit: <strong>${alert.circuit.ip_address}</strong></p>
      <p>Originating
        message <strong>${alert.origin_message.text}</strong></p>
      <p>Message sent to consumer <strong>${alert.consumer_message.text}</strong></p>
    </li>
  </div>
  % endfor
</ul>
</%def>

