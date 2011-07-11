<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>

<%def name="header()">
<title>Show all alerts</title>
${headers.loadSlickGrid(request)}
<script type="text/javascript"
        src="${a_url}/static/js/site/alertPage.js">
</script>
</%def>

<%def name="content()">
<div id="alert-grid"></div>
</%def>

