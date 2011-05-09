<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>

<%def name="header()">
   <title></title>
   ${headers.loadSlickGrid(request)} 
   
   <script type="text/javascript" src="${a_url}/static/js/site/showMeters.js"></script>
   <style type="text/css" media="screen">
     #meterGrid { height: 300px; }
   </style>   
   <script type="text/javascript">
     $(function() { 
       loadPage(${meters});
     });     
   </script>

</%def>

<%def name="content()">
<div id="meterGrid">
</div>

</%def>
