<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>

<%def name="header()">
<title>Show all gaps</title>
${headers.loadSlickGrid(request)}
<script type="text/javascript"
        src="${a_url}/static/js/site/gapPage.js">
</script>
<script type="text/javascript"> 
  $(document).ready(loadGrid);
</script>
</%def>

<%! 
   from datetime import datetime, timedelta
   tomorrow= datetime.now() + timedelta(days=1)
   today = datetime.now()
%>

<%def name="content()">

NOTE:  Selecting an End Date beyond today will include 'active' gaps
<br>
<br>
<form method="POST" id="gap_form" action="">
  Start Date: <input id="start" type="text" name="start" value="${today.strftime("%m/%d/%Y")}" />
  End Date: <input id="end" type="text" name="end" value="${tomorrow.strftime("%m/%d/%Y")}" />
  Gap (Seconds): <input id="gap" type="text" name="gap" value="5400" />
  <a href="javascript:loadGrid()">GO</a>
</form>
<br>

<div id="gap-grid"></div>
</%def>

