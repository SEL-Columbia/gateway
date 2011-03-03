<%inherit file="../base.mako"/>

<%def name="header()">
<title>Manage ${cls.__name__}</title>
<script type="text/javascript">
  $(function() { 
    $("#button").button();
  });
</script>
</%def>

<%def name="content()">
<a id="button"
   href="${request.application_url}/add/${cls.__name__}">
   Add a ${cls.__name__}</a>
<div class="center-table">
   ${grid.render()}
</div>      
</%def>
