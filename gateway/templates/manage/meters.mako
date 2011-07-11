<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>

<%def name="header()">
   <title></title>
   ${headers.loadSlickGrid(request)} 
   
   <script type="text/javascript" src="${a_url}/static/js/site/showMeters.js"></script>
   <style type="text/css" media="screen">
     #meterGrid { height: 500px; }
     #add-meter { margin-bottom: 20px; } 
   </style>   

   <script type="text/javascript">
     <%! 
        import simplejson
      %>
     $(function() { 
         loadPage();
        $("a#add-meter").button();
     });     
   </script>

</%def>

<%def name="content()">
<a id="add-meter" href="${a_url}/manage/add_meter">Add a new meter</a>

<div id="meterGrid">
</div>

</%def>
