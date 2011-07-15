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
      ${alert}
  </div>
  % endfor
</ul>
</%def>

