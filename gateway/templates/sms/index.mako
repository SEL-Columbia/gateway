## -*- coding: utf-8 -*-

<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>
<%! 
   import simplejson
   from datetime import datetime
   from gateway.utils import Widget
  
%> 


<%def name="header()"> 
   <title>SMS logs</title>

   <style type="text/css" media="screen">
     a { color: #004276; }      
   </style>   

   <script type="text/javascript">


     $(function() {
        $('#tabs').tabs();
        $('.widgets').setWidget('.widget');
     });
   </script>             
</%def>

<%def name="content()"> 
  <p>Current time on
  server: <strong>${datetime.now().ctime()}</strong> </p>
  <p>Total number of messages: <strong>${count}</strong></p>
  <a href="${request.application_url}/sms/received">
       View outgoing queue</a>
   <form method="GET" id="" 
         action="${request.application_url}/sms/index">
     <input type="text" name="limit" value="${limit}" />
     <input type="submit" name="" value="Limit messages" />
   </form>
<p>All messages, ordered by date.</p>
<div class="messages">
  <table>
    <thead>
      <th>Message id</th>
      <th>Text</th>
      <th>Phone number</th>
      <th>Date</th>
      <th>Message Type</th>
    </thead>
    <tbody> 
      % for msg in messages: 
      <tr>
        <td>${msg.id}</td>
        <td><a style="color: #004276; font-weight: bold"
               href="${a_url}/message/index/${msg.uuid}">
            ${msg.text}
        </a></td>
        <td>${msg.number}</td>
        <td>${msg.date.ctime()}</td>
        <td>${msg.type}</td>
      </tr>
      % endfor           
    </tbody>
  </table>
</%def>
