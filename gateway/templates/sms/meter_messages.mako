<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>

<%def name="header()">
<style type="text/css" media="screen">
  a { color: 
</style>
</%def>    

<%def name="content()">
<p>These are all of the messages <strong>from</strong> meter configured in the
  system</p>
<table>
  <tr>
    <th>Meter name</th>
    <th>Message text</th>
    <th>Message date</th>
  </tr>
  % for message in results: 
  <tr>
    <td><a href="/meter/index/${message[1]}">${message[0]}</a></td>
    <td>${message[2]}</td>
    <td>${message[3].ctime()}</td>
  </tr>
  % endfor
  

</table>

</%def>

